from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region


class DS3LocationCategory(IntEnum):
    WEAPON = 0
    SHIELD = 1
    ARMOR = 2
    RING = 3
    SPELL = 4
    NPC = 5
    KEY = 6
    BOSS = 7
    MISC = 8
    HEALTH = 9
    PROGRESSIVE_ITEM = 10
    EVENT = 11


class DS3LocationData(NamedTuple):
    name: str
    default_item: str
    category: DS3LocationCategory


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"
    category: DS3LocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DS3LocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 100

        table_order = [
            "Firelink Shrine",
            "Firelink Shrine Bell Tower",
            "High Wall of Lothric",
            "Undead Settlement",
            "Road of Sacrifices",
            "Cathedral of the Deep",
            "Farron Keep",
            "Catacombs of Carthus",
            "Smouldering Lake",
            "Irithyll of the Boreal Valley",
            "Irithyll Dungeon",
            "Profaned Capital",
            "Anor Londo",
            "Lothric Castle",
            "Consumed King's Garden",
            "Grand Archives",
            "Untended Graves",
            "Archdragon Peak",

            "Painted World of Ariandel 1",
            "Painted World of Ariandel 2",
            "Dreg Heap",
            "Ringed City",

            "Progressive Items 1",
            "Progressive Items 2",
            "Progressive Items 3",
            "Progressive Items 4",
            "Progressive Items DLC",
            "Progressive Items Health",
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output


location_tables = {
    "Firelink Shrine": [
        DS3LocationData("FS: Broken Straight Sword",               "Broken Straight Sword",             DS3LocationCategory.WEAPON),
        DS3LocationData("FS: East-West Shield",                    "East-West Shield",                  DS3LocationCategory.SHIELD),
        DS3LocationData("FS: Uchigatana",                          "Uchigatana",                        DS3LocationCategory.WEAPON),
        DS3LocationData("FS: Master's Attire",                     "Master's Attire",                   DS3LocationCategory.ARMOR),
        DS3LocationData("FS: Master's Gloves",                     "Master's Gloves",                   DS3LocationCategory.ARMOR),
    ],
    "Firelink Shrine Bell Tower": [
        DS3LocationData("FSBT: Covetous Silver Serpent Ring",      "Covetous Silver Serpent Ring",      DS3LocationCategory.RING),
        DS3LocationData("FSBT: Fire Keeper Robe",                  "Fire Keeper Robe",                  DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Fire Keeper Gloves",                "Fire Keeper Gloves",                DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Fire Keeper Skirt",                 "Fire Keeper Skirt",                 DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Estus Ring",                        "Estus Ring",                        DS3LocationCategory.RING),
        DS3LocationData("FSBT: Fire Keeper Soul",                  "Fire Keeper Soul",                  DS3LocationCategory.MISC),
    ],
    "High Wall of Lothric": [
        DS3LocationData("HWL: Deep Battle Axe",                    "Deep Battle Axe",                   DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Club",                               "Club",                              DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Claymore",                           "Claymore",                          DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Binoculars",                         "Binoculars",                        DS3LocationCategory.MISC),
        DS3LocationData("HWL: Longbow",                            "Longbow",                           DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Mail Breaker",                       "Mail Breaker",                      DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Broadsword",                         "Broadsword",                        DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Silver Eagle Kite Shield",           "Silver Eagle Kite Shield",          DS3LocationCategory.SHIELD),
        DS3LocationData("HWL: Astora's Straight Sword",            "Astora's Straight Sword",           DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Cell Key",                           "Cell Key",                          DS3LocationCategory.KEY),
        DS3LocationData("HWL: Rapier",                             "Rapier",                            DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Lucerne",                            "Lucerne",                           DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Small Lothric Banner",               "Small Lothric Banner",              DS3LocationCategory.KEY),
        DS3LocationData("HWL: Basin of Vows",                      "Basin of Vows",                     DS3LocationCategory.KEY),
        DS3LocationData("HWL: Soul of Boreal Valley Vordt",        "Soul of Boreal Valley Vordt",       DS3LocationCategory.BOSS),
        DS3LocationData("HWL: Soul of the Dancer",                 "Soul of the Dancer",                DS3LocationCategory.BOSS),
        DS3LocationData("HWL: Way of Blue",                        "Way of Blue",                       DS3LocationCategory.MISC),
        DS3LocationData("HWL: Greirat's Ashes",                    "Greirat's Ashes",                   DS3LocationCategory.NPC),
        DS3LocationData("HWL: Blue Tearstone Ring",                "Blue Tearstone Ring",               DS3LocationCategory.NPC),
    ],
    "Undead Settlement": [
        DS3LocationData("US: Small Leather Shield",                "Small Leather Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("US: Whip",                                "Whip",                              DS3LocationCategory.WEAPON),
        DS3LocationData("US: Reinforced Club",                     "Reinforced Club",                   DS3LocationCategory.WEAPON),
        DS3LocationData("US: Blue Wooden Shield",                  "Blue Wooden Shield",                DS3LocationCategory.SHIELD),
        DS3LocationData("US: Cleric Hat",                          "Cleric Hat",                        DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Blue Robe",                    "Cleric Blue Robe",                  DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Gloves",                       "Cleric Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Trousers",                     "Cleric Trousers",                   DS3LocationCategory.ARMOR),
        DS3LocationData("US: Mortician's Ashes",                   "Mortician's Ashes",                 DS3LocationCategory.KEY),
        DS3LocationData("US: Caestus",                             "Caestus",                           DS3LocationCategory.WEAPON),
        DS3LocationData("US: Plank Shield",                        "Plank Shield",                      DS3LocationCategory.SHIELD),
        DS3LocationData("US: Flame Stoneplate Ring",               "Flame Stoneplate Ring",             DS3LocationCategory.RING),
        DS3LocationData("US: Caduceus Round Shield",               "Caduceus Round Shield",             DS3LocationCategory.SHIELD),
        DS3LocationData("US: Fire Clutch Ring",                    "Fire Clutch Ring",                  DS3LocationCategory.RING),
        DS3LocationData("US: Partizan",                            "Partizan",                          DS3LocationCategory.WEAPON),
        DS3LocationData("US: Bloodbite Ring",                      "Bloodbite Ring",                    DS3LocationCategory.RING),
        DS3LocationData("US: Red Hilted Halberd",                  "Red Hilted Halberd",                DS3LocationCategory.WEAPON),
        DS3LocationData("US: Saint's Talisman",                    "Saint's Talisman",                  DS3LocationCategory.WEAPON),
        DS3LocationData("US: Irithyll Straight Sword",             "Irithyll Straight Sword",           DS3LocationCategory.WEAPON),
        DS3LocationData("US: Large Club",                          "Large Club",                        DS3LocationCategory.WEAPON),
        DS3LocationData("US: Northern Helm",                       "Northern Helm",                     DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Armor",                      "Northern Armor",                    DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Gloves",                     "Northern Gloves",                   DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Trousers",                   "Northern Trousers",                 DS3LocationCategory.ARMOR),
        DS3LocationData("US: Flynn's Ring",                        "Flynn's Ring",                      DS3LocationCategory.RING),
        DS3LocationData("US: Mirrah Vest",                         "Mirrah Vest",                       DS3LocationCategory.ARMOR),
        DS3LocationData("US: Mirrah Gloves",                       "Mirrah Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("US: Mirrah Trousers",                     "Mirrah Trousers",                   DS3LocationCategory.ARMOR),
        DS3LocationData("US: Chloranthy Ring",                     "Chloranthy Ring",                   DS3LocationCategory.RING),
        DS3LocationData("US: Loincloth",                           "Loincloth",                         DS3LocationCategory.ARMOR),
        DS3LocationData("US: Wargod Wooden Shield",                "Wargod Wooden Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("US: Loretta's Bone",                      "Loretta's Bone",                    DS3LocationCategory.KEY),
        DS3LocationData("US: Hand Axe",                            "Hand Axe",                          DS3LocationCategory.WEAPON),
        DS3LocationData("US: Great Scythe",                        "Great Scythe",                      DS3LocationCategory.WEAPON),
        DS3LocationData("US: Soul of the Rotted Greatwood",        "Soul of the Rotted Greatwood",      DS3LocationCategory.BOSS),
        DS3LocationData("US: Hawk Ring",                           "Hawk Ring",                         DS3LocationCategory.RING),
        DS3LocationData("US: Warrior of Sunlight",                 "Warrior of Sunlight",               DS3LocationCategory.MISC),
        DS3LocationData("US: Blessed Red and White Shield+1",      "Blessed Red and White Shield+1",    DS3LocationCategory.SHIELD),
        DS3LocationData("US: Irina's Ashes",                       "Irina's Ashes",                     DS3LocationCategory.NPC),
        DS3LocationData("US: Cornyx's Ashes",                      "Cornyx's Ashes",                    DS3LocationCategory.NPC),
        DS3LocationData("US: Cornyx's Wrap",                       "Cornyx's Wrap",                     DS3LocationCategory.NPC),
        DS3LocationData("US: Cornyx's Garb",                       "Cornyx's Garb",                     DS3LocationCategory.NPC),
        DS3LocationData("US: Cornyx's Skirt",                      "Cornyx's Skirt",                    DS3LocationCategory.NPC),
        DS3LocationData("US: Pyromancy Flame",                     "Pyromancy Flame",                   DS3LocationCategory.NPC),
        DS3LocationData("US: Transposing Kiln",                    "Transposing Kiln",                  DS3LocationCategory.MISC),
        DS3LocationData("US: Tower Key",                           "Tower Key",                         DS3LocationCategory.NPC),
    ],
    "Road of Sacrifices": [
        DS3LocationData("RS: Brigand Twindaggers",                 "Brigand Twindaggers",               DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Brigand Hood",                        "Brigand Hood",                      DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Armor",                       "Brigand Armor",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Gauntlets",                   "Brigand Gauntlets",                 DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Trousers",                    "Brigand Trousers",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Butcher Knife",                       "Butcher Knife",                     DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Brigand Axe",                         "Brigand Axe",                       DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Braille Divine Tome of Carim",        "Braille Divine Tome of Carim",      DS3LocationCategory.MISC),
        DS3LocationData("RS: Morne's Ring",                        "Morne's Ring",                      DS3LocationCategory.RING),
        DS3LocationData("RS: Twin Dragon Greatshield",             "Twin Dragon Greatshield",           DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Heretic's Staff",                     "Heretic's Staff",                   DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Sorcerer Hood",                       "Sorcerer Hood",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sorcerer Robe",                       "Sorcerer Robe",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sorcerer Gloves",                     "Sorcerer Gloves",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sorcerer Trousers",                   "Sorcerer Trousers",                 DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sage Ring",                           "Sage Ring",                         DS3LocationCategory.RING),
        DS3LocationData("RS: Fallen Knight Helm",                  "Fallen Knight Helm",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Armor",                 "Fallen Knight Armor",               DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Gauntlets",             "Fallen Knight Gauntlets",           DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Trousers",              "Fallen Knight Trousers",            DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Hood",                     "Conjurator Hood",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Robe",                     "Conjurator Robe",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Manchettes",               "Conjurator Manchettes",             DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Boots",                    "Conjurator Boots",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Great Swamp Pyromancy Tome",          "Great Swamp Pyromancy Tome",        DS3LocationCategory.MISC),
        DS3LocationData("RS: Great Club",                          "Great Club",                        DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Exile Greatsword",                    "Exile Greatsword",                  DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Farron Coal",                         "Farron Coal",                       DS3LocationCategory.MISC),
        DS3LocationData("RS: Sellsword Twinblades",                "Sellsword Twinblades",              DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Sellsword Helm",                      "Sellsword Helm",                    DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Armor",                     "Sellsword Armor",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Gauntlet",                  "Sellsword Gauntlet",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Trousers",                  "Sellsword Trousers",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Golden Falcon Shield",                "Golden Falcon Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Herald Helm",                         "Herald Helm",                       DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Herald Armor",                        "Herald Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Herald Gloves",                       "Herald Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Herald Trousers",                     "Herald Trousers",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Grass Crest Shield",                  "Grass Crest Shield",                DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Soul of a Crystal Sage",              "Soul of a Crystal Sage",            DS3LocationCategory.BOSS),
        DS3LocationData("RS: Great Swamp Ring",                    "Great Swamp Ring",                  DS3LocationCategory.RING),
        DS3LocationData("RS: Orbeck's Ashes",                      "Orbeck's Ashes",                    DS3LocationCategory.NPC),
    ],
    "Cathedral of the Deep": [
        DS3LocationData("CD: Paladin's Ashes",                     "Paladin's Ashes",                   DS3LocationCategory.MISC),
        DS3LocationData("CD: Spider Shield",                       "Spider Shield",                     DS3LocationCategory.SHIELD),
        DS3LocationData("CD: Crest Shield",                        "Crest Shield",                      DS3LocationCategory.SHIELD),
        DS3LocationData("CD: Notched Whip",                        "Notched Whip",                      DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Astora Greatsword",                   "Astora Greatsword",                 DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Executioner's Greatsword",            "Executioner's Greatsword",          DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Curse Ward Greatshield",              "Curse Ward Greatshield",            DS3LocationCategory.SHIELD),
        DS3LocationData("CD: Saint-tree Bellvine",                 "Saint-tree Bellvine",               DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Poisonbite Ring",                     "Poisonbite Ring",                   DS3LocationCategory.RING),
        DS3LocationData("CD: Lloyd's Sword Ring",                  "Lloyd's Sword Ring",                DS3LocationCategory.RING),
        DS3LocationData("CD: Seek Guidance",                       "Seek Guidance",                     DS3LocationCategory.SPELL),
        DS3LocationData("CD: Aldrich's Sapphire",                  "Aldrich's Sapphire",                DS3LocationCategory.RING),
        DS3LocationData("CD: Deep Braille Divine Tome",            "Deep Braille Divine Tome",          DS3LocationCategory.MISC),
        DS3LocationData("CD: Saint Bident",                        "Saint Bident",                      DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Maiden Hood",                         "Maiden Hood",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Robe",                         "Maiden Robe",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Gloves",                       "Maiden Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Skirt",                        "Maiden Skirt",                      DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Drang Armor",                         "Drang Armor",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Drang Gauntlets",                     "Drang Gauntlets",                   DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Drang Shoes",                         "Drang Shoes",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Drang Hammers",                       "Drang Hammers",                     DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Deep Ring",                           "Deep Ring",                         DS3LocationCategory.RING),
        DS3LocationData("CD: Archdeacon White Crown",              "Archdeacon White Crown",            DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Archdeacon Holy Garb",                "Archdeacon Holy Garb",              DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Archdeacon Skirt",                    "Archdeacon Skirt",                  DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Arbalest",                            "Arbalest",                          DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Small Doll",                          "Small Doll",                        DS3LocationCategory.KEY),
        DS3LocationData("CD: Soul of the Deacons of the Deep",     "Soul of the Deacons of the Deep",   DS3LocationCategory.BOSS),
        DS3LocationData("CD: Rosaria's Fingers",                   "Rosaria's Fingers",                 DS3LocationCategory.MISC)
    ],
    "Farron Keep": [
        DS3LocationData("FK: Ragged Mask",                         "Ragged Mask",                       DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Iron Flesh",                          "Iron Flesh",                        DS3LocationCategory.SPELL),
        DS3LocationData("FK: Golden Scroll",                       "Golden Scroll",                     DS3LocationCategory.MISC),
        DS3LocationData("FK: Antiquated Dress",                    "Antiquated Dress",                  DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Antiquated Gloves",                   "Antiquated Gloves",                 DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Antiquated Skirt",                    "Antiquated Skirt",                  DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Helm",                "Nameless Knight Helm",              DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Armor",               "Nameless Knight Armor",             DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Gauntlets",           "Nameless Knight Gauntlets",         DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Leggings",            "Nameless Knight Leggings",          DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Sunlight Talisman",                   "Sunlight Talisman",                 DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Wolf's Blood Swordgrass",             "Wolf's Blood Swordgrass",           DS3LocationCategory.MISC),
        DS3LocationData("FK: Greatsword",                          "Greatsword",                        DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Sage's Coal",                         "Sage's Coal",                       DS3LocationCategory.MISC),
        DS3LocationData("FK: Stone Parma",                         "Stone Parma",                       DS3LocationCategory.SHIELD),
        DS3LocationData("FK: Sage's Scroll",                       "Sage's Scroll",                     DS3LocationCategory.MISC),
        DS3LocationData("FK: Crown of Dusk",                       "Crown of Dusk",                     DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Lingering Dragoncrest Ring",          "Lingering Dragoncrest Ring",        DS3LocationCategory.RING),
        DS3LocationData("FK: Pharis's Hat",                        "Pharis's Hat",                      DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Black Bow of Pharis",                 "Black Bow of Pharis",               DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Dreamchaser's Ashes",                 "Dreamchaser's Ashes",               DS3LocationCategory.MISC),
        DS3LocationData("FK: Great Axe",                           "Great Axe",                         DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Dragon Crest Shield",                 "Dragon Crest Shield",               DS3LocationCategory.SHIELD),
        DS3LocationData("FK: Lightning Spear",                     "Lightning Spear",                   DS3LocationCategory.SPELL),
        DS3LocationData("FK: Atonement",                           "Atonement",                         DS3LocationCategory.SPELL),
        DS3LocationData("FK: Great Magic Weapon",                  "Great Magic Weapon",                DS3LocationCategory.SPELL),
        DS3LocationData("FK: Cinders of a Lord - Abyss Watcher",   "Cinders of a Lord - Abyss Watcher", DS3LocationCategory.KEY),
        DS3LocationData("FK: Soul of the Blood of the Wolf",       "Soul of the Blood of the Wolf",     DS3LocationCategory.BOSS),
        DS3LocationData("FK: Soul of a Stray Demon",               "Soul of a Stray Demon",             DS3LocationCategory.BOSS),
        DS3LocationData("FK: Watchdogs of Farron",                 "Watchdogs of Farron",               DS3LocationCategory.MISC),
    ],
    "Catacombs of Carthus": [
        DS3LocationData("CC: Carthus Pyromancy Tome",              "Carthus Pyromancy Tome",            DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Milkring",                    "Carthus Milkring",                  DS3LocationCategory.RING),
        DS3LocationData("CC: Grave Warden's Ashes",                "Grave Warden's Ashes",              DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Bloodring",                   "Carthus Bloodring",                 DS3LocationCategory.RING),
        DS3LocationData("CC: Grave Warden Pyromancy Tome",         "Grave Warden Pyromancy Tome",       DS3LocationCategory.MISC),
        DS3LocationData("CC: Old Sage's Blindfold",                "Old Sage's Blindfold",              DS3LocationCategory.ARMOR),
        DS3LocationData("CC: Witch's Ring",                        "Witch's Ring",                      DS3LocationCategory.RING),
        DS3LocationData("CC: Black Blade",                         "Black Blade",                       DS3LocationCategory.WEAPON),
        DS3LocationData("CC: Soul of High Lord Wolnir",            "Soul of High Lord Wolnir",          DS3LocationCategory.BOSS),
        DS3LocationData("CC: Soul of a Demon",                     "Soul of a Demon",                   DS3LocationCategory.BOSS),
    ],
    "Smouldering Lake": [
        DS3LocationData("SL: Shield of Want",                      "Shield of Want",                    DS3LocationCategory.SHIELD),
        DS3LocationData("SL: Speckled Stoneplate Ring",            "Speckled Stoneplate Ring",          DS3LocationCategory.RING),
        DS3LocationData("SL: Dragonrider Bow",                     "Dragonrider Bow",                   DS3LocationCategory.WEAPON),
        DS3LocationData("SL: Lightning Stake",                     "Lightning Stake",                   DS3LocationCategory.SPELL),
        DS3LocationData("SL: Izalith Pyromancy Tome",              "Izalith Pyromancy Tome",            DS3LocationCategory.MISC),
        DS3LocationData("SL: Black Knight Sword",                  "Black Knight Sword",                DS3LocationCategory.WEAPON),
        DS3LocationData("SL: Quelana Pyromancy Tome",              "Quelana Pyromancy Tome",            DS3LocationCategory.MISC),
        DS3LocationData("SL: Toxic Mist",                          "Toxic Mist",                        DS3LocationCategory.SPELL),
        DS3LocationData("SL: White Hair Talisman",                 "White Hair Talisman",               DS3LocationCategory.WEAPON),
        DS3LocationData("SL: Izalith Staff",                       "Izalith Staff",                     DS3LocationCategory.WEAPON),
        DS3LocationData("SL: Sacred Flame",                        "Sacred Flame",                      DS3LocationCategory.SPELL),
        DS3LocationData("SL: Fume Ultra Greatsword",               "Fume Ultra Greatsword",             DS3LocationCategory.WEAPON),
        DS3LocationData("SL: Black Iron Greatshield",              "Black Iron Greatshield",            DS3LocationCategory.SHIELD),
        DS3LocationData("SL: Soul of the Old Demon King",          "Soul of the Old Demon King",        DS3LocationCategory.BOSS),
        DS3LocationData("SL: Knight Slayer's Ring",                "Knight Slayer's Ring",              DS3LocationCategory.RING),
    ],
    "Irithyll of the Boreal Valley": [
        DS3LocationData("IBV: Dorhys' Gnawing",                    "Dorhys' Gnawing",                   DS3LocationCategory.SPELL),
        DS3LocationData("IBV: Witchtree Branch",                   "Witchtree Branch",                  DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Magic Clutch Ring",                  "Magic Clutch Ring",                 DS3LocationCategory.RING),
        DS3LocationData("IBV: Ring of the Sun's First Born",       "Ring of the Sun's First Born",      DS3LocationCategory.RING),
        DS3LocationData("IBV: Roster of Knights",                  "Roster of Knights",                 DS3LocationCategory.MISC),
        DS3LocationData("IBV: Pontiff's Right Eye",                "Pontiff's Right Eye",               DS3LocationCategory.RING),
        DS3LocationData("IBV: Yorshka's Spear",                    "Yorshka's Spear",                   DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Great Heal",                         "Great Heal",                        DS3LocationCategory.SPELL),
        DS3LocationData("IBV: Smough's Great Hammer",              "Smough's Great Hammer",             DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Leo Ring",                           "Leo Ring",                          DS3LocationCategory.RING),
        DS3LocationData("IBV: Excrement-covered Ashes",            "Excrement-covered Ashes",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Dark Stoneplate Ring",               "Dark Stoneplate Ring",              DS3LocationCategory.RING),
        DS3LocationData("IBV: Easterner's Ashes",                  "Easterner's Ashes",                 DS3LocationCategory.MISC),
        DS3LocationData("IBV: Painting Guardian's Curved Sword",   "Painting Guardian's Curved Sword",  DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Painting Guardian Hood",             "Painting Guardian Hood",            DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Painting Guardian Gown",             "Painting Guardian Gown",            DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Painting Guardian Gloves",           "Painting Guardian Gloves",          DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Painting Guardian Waistcloth",       "Painting Guardian Waistcloth",      DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Dragonslayer Greatbow",              "Dragonslayer Greatbow",             DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Reversal Ring",                      "Reversal Ring",                     DS3LocationCategory.RING),
        DS3LocationData("IBV: Brass Helm",                         "Brass Helm",                        DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Brass Armor",                        "Brass Armor",                       DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Brass Gauntlets",                    "Brass Gauntlets",                   DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Brass Leggings",                     "Brass Leggings",                    DS3LocationCategory.ARMOR),
        DS3LocationData("IBV: Ring of Favor",                      "Ring of Favor",                     DS3LocationCategory.RING),
        DS3LocationData("IBV: Golden Ritual Spear",                "Golden Ritual Spear",               DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Soul of Pontiff Sulyvahn",           "Soul of Pontiff Sulyvahn",          DS3LocationCategory.BOSS),
        DS3LocationData("IBV: Aldrich Faithful",                   "Aldrich Faithful",                  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Drang Twinspears",                   "Drang Twinspears",                  DS3LocationCategory.WEAPON),
    ],
    "Irithyll Dungeon": [
        DS3LocationData("ID: Bellowing Dragoncrest Ring",          "Bellowing Dragoncrest Ring",        DS3LocationCategory.RING),
        DS3LocationData("ID: Jailbreaker's Key",                   "Jailbreaker's Key",                 DS3LocationCategory.KEY),
        DS3LocationData("ID: Prisoner Chief's Ashes",              "Prisoner Chief's Ashes",            DS3LocationCategory.KEY),
        DS3LocationData("ID: Old Sorcerer Hat",                    "Old Sorcerer Hat",                  DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Coat",                   "Old Sorcerer Coat",                 DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Gauntlets",              "Old Sorcerer Gauntlets",            DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Boots",                  "Old Sorcerer Boots",                DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Great Magic Shield",                  "Great Magic Shield",                DS3LocationCategory.SPELL),
        DS3LocationData("ID: Dragon Torso Stone",                  "Dragon Torso Stone",                DS3LocationCategory.MISC),
        DS3LocationData("ID: Lightning Blade",                     "Lightning Blade",                   DS3LocationCategory.SPELL),
        DS3LocationData("ID: Profaned Coal",                       "Profaned Coal",                     DS3LocationCategory.MISC),
        DS3LocationData("ID: Xanthous Ashes",                      "Xanthous Ashes",                    DS3LocationCategory.MISC),
        DS3LocationData("ID: Old Cell Key",                        "Old Cell Key",                      DS3LocationCategory.KEY),
        DS3LocationData("ID: Pickaxe",                             "Pickaxe",                           DS3LocationCategory.WEAPON),
        DS3LocationData("ID: Profaned Flame",                      "Profaned Flame",                    DS3LocationCategory.SPELL),
        DS3LocationData("ID: Covetous Gold Serpent Ring",          "Covetous Gold Serpent Ring",        DS3LocationCategory.RING),
        DS3LocationData("ID: Jailer's Key Ring",                   "Jailer's Key Ring",                 DS3LocationCategory.KEY),
        DS3LocationData("ID: Dusk Crown Ring",                     "Dusk Crown Ring",                   DS3LocationCategory.RING),
        DS3LocationData("ID: Dark Clutch Ring",                    "Dark Clutch Ring",                  DS3LocationCategory.RING),
        DS3LocationData("ID: Karla's Ashes",                       "Karla's Ashes",                     DS3LocationCategory.NPC),
        DS3LocationData("ID: Karla's Pointed Hat",                 "Karla's Pointed Hat",               DS3LocationCategory.NPC),
        DS3LocationData("ID: Karla's Coat",                        "Karla's Coat",                      DS3LocationCategory.NPC),
        DS3LocationData("ID: Karla's Gloves",                      "Karla's Gloves",                    DS3LocationCategory.NPC),
        DS3LocationData("ID: Karla's Trousers",                    "Karla's Trousers",                  DS3LocationCategory.NPC),
    ],
    "Profaned Capital": [
        DS3LocationData("PC: Cursebite Ring",                      "Cursebite Ring",                      DS3LocationCategory.RING),
        DS3LocationData("PC: Court Sorcerer Hood",                 "Court Sorcerer Hood",                 DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Robe",                 "Court Sorcerer Robe",                 DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Gloves",               "Court Sorcerer Gloves",               DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Trousers",             "Court Sorcerer Trousers",             DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Wrath of the Gods",                   "Wrath of the Gods",                   DS3LocationCategory.SPELL),
        DS3LocationData("PC: Logan's Scroll",                      "Logan's Scroll",                      DS3LocationCategory.MISC),
        DS3LocationData("PC: Eleonora",                            "Eleonora",                            DS3LocationCategory.WEAPON),
        DS3LocationData("PC: Court Sorcerer's Staff",              "Court Sorcerer's Staff",              DS3LocationCategory.WEAPON),
        DS3LocationData("PC: Greatshield of Glory",                "Greatshield of Glory",                DS3LocationCategory.SHIELD),
        DS3LocationData("PC: Storm Ruler",                         "Storm Ruler",                         DS3LocationCategory.KEY),
        DS3LocationData("PC: Cinders of a Lord - Yhorm the Giant", "Cinders of a Lord - Yhorm the Giant", DS3LocationCategory.KEY),
        DS3LocationData("PC: Soul of Yhorm the Giant",             "Soul of Yhorm the Giant",             DS3LocationCategory.BOSS),
    ],
    "Anor Londo": [
        DS3LocationData("AL: Giant's Coal",                        "Giant's Coal",                        DS3LocationCategory.MISC),
        DS3LocationData("AL: Sun Princess Ring",                   "Sun Princess Ring",                   DS3LocationCategory.RING),
        DS3LocationData("AL: Aldrich's Ruby",                      "Aldrich's Ruby",                      DS3LocationCategory.RING),
        DS3LocationData("AL: Cinders of a Lord - Aldrich",         "Cinders of a Lord - Aldrich",         DS3LocationCategory.KEY),
        DS3LocationData("AL: Soul of Aldrich",                     "Soul of Aldrich",                     DS3LocationCategory.BOSS),
    ],
    "Lothric Castle": [
        DS3LocationData("LC: Hood of Prayer",                      "Hood of Prayer",                      DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Robe of Prayer",                      "Robe of Prayer",                      DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Skirt of Prayer",                     "Skirt of Prayer",                     DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Sacred Bloom Shield",                 "Sacred Bloom Shield",                 DS3LocationCategory.SHIELD),
        DS3LocationData("LC: Winged Knight Helm",                  "Winged Knight Helm",                  DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Winged Knight Armor",                 "Winged Knight Armor",                 DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Winged Knight Gauntlets",             "Winged Knight Gauntlets",             DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Winged Knight Leggings",              "Winged Knight Leggings",              DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Greatlance",                          "Greatlance",                          DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Sniper Crossbow",                     "Sniper Crossbow",                     DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Spirit Tree Crest Shield",            "Spirit Tree Crest Shield",            DS3LocationCategory.SHIELD),
        DS3LocationData("LC: Red Tearstone Ring",                  "Red Tearstone Ring",                  DS3LocationCategory.RING),
        DS3LocationData("LC: Caitha's Chime",                      "Caitha's Chime",                      DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Braille Divine Tome of Lothric",      "Braille Divine Tome of Lothric",      DS3LocationCategory.MISC),
        DS3LocationData("LC: Knight's Ring",                       "Knight's Ring",                       DS3LocationCategory.RING),
        DS3LocationData("LC: Irithyll Rapier",                     "Irithyll Rapier",                     DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Sunlight Straight Sword",             "Sunlight Straight Sword",             DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Soul of Dragonslayer Armour",         "Soul of Dragonslayer Armour",         DS3LocationCategory.BOSS),
        DS3LocationData("LC: Grand Archives Key",                  "Grand Archives Key",                  DS3LocationCategory.KEY),
        DS3LocationData("LC: Gotthard Twinswords",                 "Gotthard Twinswords",                 DS3LocationCategory.WEAPON),
    ],
    "Consumed King's Garden": [
        DS3LocationData("CKG: Dragonscale Ring",                   "Dragonscale Ring",                        DS3LocationCategory.RING),
        DS3LocationData("CKG: Shadow Mask",                        "Shadow Mask",                             DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Garb",                        "Shadow Garb",                             DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Gauntlets",                   "Shadow Gauntlets",                        DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Leggings",                    "Shadow Leggings",                         DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Claw",                               "Claw",                                    DS3LocationCategory.WEAPON),
        DS3LocationData("CKG: Soul of Consumed Oceiros",           "Soul of Consumed Oceiros",                DS3LocationCategory.BOSS),
        DS3LocationData("CKG: Magic Stoneplate Ring",              "Magic Stoneplate Ring",                   DS3LocationCategory.RING),
    ],
    "Grand Archives": [
        DS3LocationData("GA: Avelyn",                              "Avelyn",                                  DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Witch's Locks",                       "Witch's Locks",                           DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Power Within",                        "Power Within",                            DS3LocationCategory.SPELL),
        DS3LocationData("GA: Scholar Ring",                        "Scholar Ring",                            DS3LocationCategory.RING),
        DS3LocationData("GA: Soul Stream",                         "Soul Stream",                             DS3LocationCategory.SPELL),
        DS3LocationData("GA: Fleshbite Ring",                      "Fleshbite Ring",                          DS3LocationCategory.RING),
        DS3LocationData("GA: Crystal Chime",                       "Crystal Chime",                           DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Golden Wing Crest Shield",            "Golden Wing Crest Shield",                DS3LocationCategory.SHIELD),
        DS3LocationData("GA: Onikiri and Ubadachi",                "Onikiri and Ubadachi",                    DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Hunter's Ring",                       "Hunter's Ring",                           DS3LocationCategory.RING),
        DS3LocationData("GA: Divine Pillars of Light",             "Divine Pillars of Light",                 DS3LocationCategory.SPELL),
        DS3LocationData("GA: Cinders of a Lord - Lothric Prince",  "Cinders of a Lord - Lothric Prince",      DS3LocationCategory.KEY),
        DS3LocationData("GA: Soul of the Twin Princes",            "Soul of the Twin Princes",                DS3LocationCategory.BOSS),
        DS3LocationData("GA: Sage's Crystal Staff",                "Sage's Crystal Staff",                    DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Outrider Knight Helm",                "Outrider Knight Helm",                    DS3LocationCategory.ARMOR),
        DS3LocationData("GA: Outrider Knight Armor",               "Outrider Knight Armor",                   DS3LocationCategory.ARMOR),
        DS3LocationData("GA: Outrider Knight Gauntlets",           "Outrider Knight Gauntlets",               DS3LocationCategory.ARMOR),
        DS3LocationData("GA: Outrider Knight Leggings",            "Outrider Knight Leggings",                DS3LocationCategory.ARMOR),
        DS3LocationData("GA: Crystal Scroll",                      "Crystal Scroll",                          DS3LocationCategory.MISC),
    ],
    "Untended Graves": [
        DS3LocationData("UG: Ashen Estus Ring",                    "Ashen Estus Ring",                        DS3LocationCategory.RING),
        DS3LocationData("UG: Black Knight Glaive",                 "Black Knight Glaive",                     DS3LocationCategory.WEAPON),
        DS3LocationData("UG: Hornet Ring",                         "Hornet Ring",                             DS3LocationCategory.RING),
        DS3LocationData("UG: Chaos Blade",                         "Chaos Blade",                             DS3LocationCategory.WEAPON),
        DS3LocationData("UG: Blacksmith Hammer",                   "Blacksmith Hammer",                       DS3LocationCategory.WEAPON),
        DS3LocationData("UG: Eyes of a Fire Keeper",               "Eyes of a Fire Keeper",                   DS3LocationCategory.KEY),
        DS3LocationData("UG: Coiled Sword Fragment",               "Coiled Sword Fragment",                   DS3LocationCategory.MISC),
        DS3LocationData("UG: Soul of Champion Gundyr",             "Soul of Champion Gundyr",                 DS3LocationCategory.BOSS),
    ],
    "Archdragon Peak": [
        DS3LocationData("AP: Lightning Clutch Ring",               "Lightning Clutch Ring",                   DS3LocationCategory.RING),
        DS3LocationData("AP: Ancient Dragon Greatshield",          "Ancient Dragon Greatshield",              DS3LocationCategory.SHIELD),
        DS3LocationData("AP: Ring of Steel Protection",            "Ring of Steel Protection",                DS3LocationCategory.RING),
        DS3LocationData("AP: Calamity Ring",                       "Calamity Ring",                           DS3LocationCategory.RING),
        DS3LocationData("AP: Drakeblood Greatsword",               "Drakeblood Greatsword",                   DS3LocationCategory.WEAPON),
        DS3LocationData("AP: Dragonslayer Spear",                  "Dragonslayer Spear",                      DS3LocationCategory.WEAPON),
        DS3LocationData("AP: Thunder Stoneplate Ring",             "Thunder Stoneplate Ring",                 DS3LocationCategory.RING),
        DS3LocationData("AP: Great Magic Barrier",                 "Great Magic Barrier",                     DS3LocationCategory.SPELL),
        DS3LocationData("AP: Dragon Chaser's Ashes",               "Dragon Chaser's Ashes",                   DS3LocationCategory.MISC),
        DS3LocationData("AP: Twinkling Dragon Torso Stone",        "Twinkling Dragon Torso Stone",            DS3LocationCategory.MISC),
        DS3LocationData("AP: Dragonslayer Helm",                   "Dragonslayer Helm",                       DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Armor",                  "Dragonslayer Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Gauntlets",              "Dragonslayer Gauntlets",                  DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Leggings",               "Dragonslayer Leggings",                   DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Ricard's Rapier",                     "Ricard's Rapier",                         DS3LocationCategory.WEAPON),
        DS3LocationData("AP: Soul of the Nameless King",           "Soul of the Nameless King",               DS3LocationCategory.BOSS),
        DS3LocationData("AP: Dragon Tooth",                        "Dragon Tooth",                            DS3LocationCategory.WEAPON),
        DS3LocationData("AP: Havel's Greatshield",                 "Havel's Greatshield",                     DS3LocationCategory.SHIELD),
    ],
    "Kiln of the First Flame": [],

    # DLC
    "Painted World of Ariandel 1": [
        DS3LocationData("PW: Follower Javelin",                    "Follower Javelin",                        DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Frozen Weapon",                       "Frozen Weapon",                           DS3LocationCategory.SPELL),
        DS3LocationData("PW: Millwood Greatbow",                   "Millwood Greatbow",                       DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Captain's Ashes",                     "Captain's Ashes",                         DS3LocationCategory.MISC),
        DS3LocationData("PW: Millwood Battle Axe",                 "Millwood Battle Axe",                     DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Ethereal Oak Shield",                 "Ethereal Oak Shield",                     DS3LocationCategory.SHIELD),
        DS3LocationData("PW: Crow Quills",                         "Crow Quills",                             DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Slave Knight Hood",                   "Slave Knight Hood",                       DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Slave Knight Armor",                  "Slave Knight Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Slave Knight Gauntlets",              "Slave Knight Gauntlets",                  DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Slave Knight Leggings",               "Slave Knight Leggings",                   DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Way of White Corona",                 "Way of White Corona",                     DS3LocationCategory.SPELL),
        DS3LocationData("PW: Crow Talons",                         "Crow Talons",                             DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Onyx Blade",                          "Onyx Blade",                              DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Contraption Key",                     "Contraption Key",                         DS3LocationCategory.KEY),
    ],
    "Painted World of Ariandel 2": [  
        DS3LocationData("PW: Quakestone Hammer",                   "Quakestone Hammer",                       DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Earth Seeker",                        "Earth Seeker",                            DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Follower Torch",                      "Follower Torch",                          DS3LocationCategory.SHIELD),
        DS3LocationData("PW: Follower Shield",                     "Follower Shield",                         DS3LocationCategory.SHIELD),
        DS3LocationData("PW: Follower Sabre",                      "Follower Sabre",                          DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Snap Freeze",                         "Snap Freeze",                             DS3LocationCategory.SPELL),
        DS3LocationData("PW: Floating Chaos",                      "Floating Chaos",                          DS3LocationCategory.SPELL),
        DS3LocationData("PW: Pyromancer's Parting Flame",          "Pyromancer's Parting Flame",              DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Vilhelm's Helm",                      "Vilhelm's Helm",                          DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Vilhelm's Armor",                     "Vilhelm's Armor",                         DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Vilhelm's Gauntlets",                 "Vilhelm's Gauntlets",                     DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Vilhelm's Leggings",                  "Vilhelm's Leggings",                      DS3LocationCategory.ARMOR),
        DS3LocationData("PW: Valorheart",                          "Valorheart",                              DS3LocationCategory.WEAPON),
        DS3LocationData("PW: Champion's Bones",                    "Champion's Bones",                        DS3LocationCategory.MISC),
        DS3LocationData("PW: Soul of Sister Friede",               "Soul of Sister Friede",                   DS3LocationCategory.BOSS),
        DS3LocationData("PW: Chillbite Ring",                      "Chillbite Ring",                          DS3LocationCategory.RING),
    ],
    "Dreg Heap": [
        DS3LocationData("DH: Loincloth",                           "Loincloth",                               DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Aquamarine Dagger",                   "Aquamarine Dagger",                       DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Murky Hand Scythe",                   "Murky Hand Scythe",                       DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Murky Longstaff",                     "Murky Longstaff",                         DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Great Soul Dregs",                    "Great Soul Dregs",                        DS3LocationCategory.SPELL),
        DS3LocationData("DH: Lothric War Banner",                  "Lothric War Banner",                      DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Projected Heal",                      "Projected Heal",                          DS3LocationCategory.SPELL),
        DS3LocationData("DH: Desert Pyromancer Hood",              "Desert Pyromancer Hood",                  DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Desert Pyromancer Garb",              "Desert Pyromancer Garb",                  DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Desert Pyromancer Gloves",            "Desert Pyromancer Gloves",                DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Desert Pyromancer Skirt",             "Desert Pyromancer Skirt",                 DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Giant Door Shield",                   "Giant Door Shield",                       DS3LocationCategory.SHIELD),
        DS3LocationData("DH: Herald Curved Greatsword",            "Herald Curved Greatsword",                DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Flame Fan",                           "Flame Fan",                               DS3LocationCategory.SPELL),
        DS3LocationData("DH: Soul of the Demon Prince",            "Soul of the Demon Prince",                DS3LocationCategory.BOSS),
        DS3LocationData("DH: Small Envoy Banner",                  "Small Envoy Banner",                      DS3LocationCategory.KEY),
        DS3LocationData("DH: Ring of Favor+3",                     "Ring of Favor+3",                         DS3LocationCategory.RING),
        DS3LocationData("DH: Covetous Silver Serpent Ring+3",      "Covetous Silver Serpent Ring+3",          DS3LocationCategory.RING),
        DS3LocationData("DH: Ring of Steel Protection+3",          "Ring of Steel Protection+3",              DS3LocationCategory.RING),
    ],
    "Ringed City": [
        DS3LocationData("RC: Ruin Sentinel Helm",                  "Ruin Sentinel Helm",                      DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Sentinel Armor",                 "Ruin Sentinel Armor",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Sentinel Gauntlets",             "Ruin Sentinel Gauntlets",                 DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Sentinel Leggings",              "Ruin Sentinel Leggings",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Black Witch Veil",                    "Black Witch Veil",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Black Witch Hat",                     "Black Witch Hat",                         DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Black Witch Garb",                    "Black Witch Garb",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Black Witch Wrappings",               "Black Witch Wrappings",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Black Witch Trousers",                "Black Witch Trousers",                    DS3LocationCategory.ARMOR),
        DS3LocationData("RC: White Preacher Head",                 "White Preacher Head",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Havel's Ring+3",                      "Havel's Ring+3",                          DS3LocationCategory.RING),
        DS3LocationData("RC: Ringed Knight Spear",                 "Ringed Knight Spear",                     DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Dragonhead Shield",                   "Dragonhead Shield",                       DS3LocationCategory.SHIELD),
        DS3LocationData("RC: Ringed Knight Straight Sword",        "Ringed Knight Straight Sword",            DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Preacher's Right Arm",                "Preacher's Right Arm",                    DS3LocationCategory.WEAPON),
        DS3LocationData("RC: White Birch Bow",                     "White Birch Bow",                         DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Church Guardian Shiv",                "Church Guardian Shiv",                    DS3LocationCategory.MISC),
        DS3LocationData("RC: Dragonhead Greatshield",              "Dragonhead Greatshield",                  DS3LocationCategory.SHIELD),
        DS3LocationData("RC: Ringed Knight Paired Greatswords",    "Ringed Knight Paired Greatswords",        DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Shira's Crown",                       "Shira's Crown",                           DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Shira's Armor",                       "Shira's Armor",                           DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Shira's Gloves",                      "Shira's Gloves",                          DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Shira's Trousers",                    "Shira's Trousers",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Crucifix of the Mad King",            "Crucifix of the Mad King",                DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Sacred Chime of Filianore",           "Sacred Chime of Filianore",               DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Iron Dragonslayer Helm",              "Iron Dragonslayer Helm",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Iron Dragonslayer Armor",             "Iron Dragonslayer Armor",                 DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Iron Dragonslayer Gauntlets",         "Iron Dragonslayer Gauntlets",             DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Iron Dragonslayer Leggings",          "Iron Dragonslayer Leggings",              DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Lightning Arrow",                     "Lightning Arrow",                         DS3LocationCategory.SPELL),
        DS3LocationData("RC: Ritual Spear Fragment",               "Ritual Spear Fragment",                   DS3LocationCategory.MISC),
        DS3LocationData("RC: Antiquated Plain Garb",               "Antiquated Plain Garb",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Violet Wrappings",                    "Violet Wrappings",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Soul of Darkeater Midir",             "Soul of Darkeater Midir",                 DS3LocationCategory.BOSS),
        DS3LocationData("RC: Soul of Slave Knight Gael",           "Soul of Slave Knight Gael",               DS3LocationCategory.BOSS),
        DS3LocationData("RC: Blood of the Dark Soul",              "Blood of the Dark Soul",                  DS3LocationCategory.KEY),
        DS3LocationData("RC: Chloranthy Ring+3",                   "Chloranthy Ring+3",                       DS3LocationCategory.RING),
        DS3LocationData("RC: Covetous Gold Serpent Ring+3",        "Covetous Gold Serpent Ring+3",            DS3LocationCategory.RING),
        DS3LocationData("RC: Ring of the Evil Eye+3",              "Ring of the Evil Eye+3",                  DS3LocationCategory.RING),
        DS3LocationData("RC: Wolf Ring+3",                         "Wolf Ring+3",                             DS3LocationCategory.RING),
    ],

    # Progressive
    "Progressive Items 1": [] +
        # Upgrade materials
        [DS3LocationData(f"Titanite Shard #{i + 1}",       "Titanite Shard",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(26)] +
        [DS3LocationData(f"Large Titanite Shard #{i + 1}", "Large Titanite Shard", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(28)] +
        [DS3LocationData(f"Titanite Slab #{i + 1}",        "Titanite Slab",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Twinkling Titanite #{i + 1}",   "Twinkling Titanite",   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(15)],

    "Progressive Items 2": [] +
        # Items
        [DS3LocationData(f"Green Blossom #{i + 1}",        "Green Blossom",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(6)] +
        [DS3LocationData(f"Firebomb #{i + 1}",             "Firebomb",             DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(4)] +
        [DS3LocationData(f"Alluring Skull #{i + 1}",       "Alluring Skull",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Undead Hunter Charm #{i + 1}",  "Undead Hunter Charm",  DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Duel Charm #{i + 1}",           "Duel Charm",           DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Throwing Knife #{i + 1}",       "Throwing Knife",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Gold Pine Resin #{i + 1}",      "Gold Pine Resin",      DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Charcoal Pine Resin #{i + 1}",  "Charcoal Pine Resin",  DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Human Pine Resin #{i + 1}",     "Human Pine Resin",     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Carthus Rouge #{i + 1}",        "Carthus Rouge",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Pale Pine Resin #{i + 1}",      "Pale Pine Resin",      DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Charcoal Pine Bundle #{i + 1}", "Charcoal Pine Bundle", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Rotten Pine Resin #{i + 1}",    "Rotten Pine Resin",    DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Homeward Bone #{i + 1}",        "Homeward Bone",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(16)] +
        [DS3LocationData(f"Pale Tongue #{i + 1}",          "Pale Tongue",          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Rusted Coin #{i + 1}",          "Rusted Coin",          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Rusted Gold Coin #{i + 1}",     "Rusted Gold Coin",     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Ember #{i + 1}",                "Ember",                DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(45)],

    "Progressive Items 3": [] +
        # Souls & Bulk Upgrade Materials
        [DS3LocationData(f"Fading Soul #{i + 1}",                       "Fading Soul",                       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Soul of a Deserted Corpse #{i + 1}",         "Soul of a Deserted Corpse",         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Large Soul of a Deserted Corpse #{i + 1}",   "Large Soul of a Deserted Corpse",   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Soul of an Unknown Traveler #{i + 1}",       "Soul of an Unknown Traveler",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Large Soul of an Unknown Traveler #{i + 1}", "Large Soul of an Unknown Traveler", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Soul of a Nameless Soldier #{i + 1}",        "Soul of a Nameless Soldier",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(4)] +
        [DS3LocationData(f"Large Soul of a Nameless Soldier #{i + 1}",  "Large Soul of a Nameless Soldier",  DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(4)] +
        [DS3LocationData(f"Soul of a Weary Warrior #{i + 1}",           "Soul of a Weary Warrior",           DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(6)] +
        [DS3LocationData(f"Soul of a Crestfallen Knight #{i + 1}",      "Soul of a Crestfallen Knight",      DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Titanite Chunk #{i + 1}",                    "Titanite Chunk",                    DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(22)] +
        [DS3LocationData(f"Titanite Scale #{i + 1}",                    "Titanite Scale",                    DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(29)],

    "Progressive Items 4": [] +
        # Gems & Random Consumables
        [DS3LocationData(f"Ring of Sacrifice #{i + 1}",                 "Ring of Sacrifice",                 DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(4)] +
        [DS3LocationData(f"Divine Blessing #{i + 1}",                   "Divine Blessing",                   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Hidden Blessing #{i + 1}",                   "Hidden Blessing",                   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Budding Green Blossom #{i + 1}",             "Budding Green Blossom",             DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Bloodred Moss Clump #{i + 1}",               "Bloodred Moss Clump",               DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Purple Moss Clump #{i + 1}",                 "Purple Moss Clump",                 DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Blooming Purple Moss Clump #{i + 1}",        "Blooming Purple Moss Clump",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Purging Stone #{i + 1}",                     "Purging Stone",                     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Rime-blue Moss Clump #{i + 1}",              "Rime-blue Moss Clump",              DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Repair Powder #{i + 1}",                     "Repair Powder",                     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Kukri #{i + 1}",                             "Kukri",                             DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Lightning Urn #{i + 1}",                     "Lightning Urn",                     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Rubbish #{i + 1}",                           "Rubbish",                           DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Blue Bug Pellet #{i + 1}",                   "Blue Bug Pellet",                   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Red Bug Pellet #{i + 1}",                    "Red Bug Pellet",                    DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Yellow Bug Pellet #{i + 1}",                 "Yellow Bug Pellet",                 DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Black Bug Pellet #{i + 1}",                  "Black Bug Pellet",                  DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Heavy Gem #{i + 1}",                         "Heavy Gem",                         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Sharp Gem #{i + 1}",                         "Sharp Gem",                         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Refined Gem #{i + 1}",                       "Refined Gem",                       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Crystal Gem #{i + 1}",                       "Crystal Gem",                       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Simple Gem #{i + 1}",                        "Simple Gem",                        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Fire Gem #{i + 1}",                          "Fire Gem",                          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Chaos Gem #{i + 1}",                         "Chaos Gem",                         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Lightning Gem #{i + 1}",                     "Lightning Gem",                     DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Deep Gem #{i + 1}",                          "Deep Gem",                          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Dark Gem #{i + 1}",                          "Dark Gem",                          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Poison Gem #{i + 1}",                        "Poison Gem",                        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Blood Gem #{i + 1}",                         "Blood Gem",                         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Raw Gem #{i + 1}",                           "Raw Gem",                           DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Blessed Gem #{i + 1}",                       "Blessed Gem",                       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Hollow Gem #{i + 1}",                        "Hollow Gem",                        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Shriving Stone #{i + 1}",                    "Shriving Stone",                    DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)],

    "Progressive Items DLC": [] +
        # Upgrade materials
        [DS3LocationData(f"Large Titanite Shard ${i + 1}", "Large Titanite Shard", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Titanite Chunk ${i + 1}",       "Titanite Chunk",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(15)] +
        [DS3LocationData(f"Titanite Slab ${i + 1}",        "Titanite Slab",        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Twinkling Titanite ${i + 1}",   "Twinkling Titanite",   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Titanite Scale ${i + 1}",       "Titanite Scale",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(11)] +


        # Items
        [DS3LocationData(f"Homeward Bone ${i + 1}", "Homeward Bone", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(6)] +
        [DS3LocationData(f"Rusted Coin ${i + 1}",   "Rusted Coin",   DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +
        [DS3LocationData(f"Ember ${i + 1}",         "Ember",         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(10)] +

        # Souls
        [DS3LocationData(f"Large Soul of an Unknown Traveler ${i + 1}",  "Large Soul of an Unknown Traveler",  DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(9)] +
        [DS3LocationData(f"Soul of a Weary Warrior ${i + 1}",            "Soul of a Weary Warrior",            DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(5)] +
        [DS3LocationData(f"Large Soul of a Weary Warrior ${i + 1}",      "Large Soul of a Weary Warrior",      DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(6)] +
        [DS3LocationData(f"Soul of a Crestfallen Knight ${i + 1}",       "Soul of a Crestfallen Knight",       DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(6)] +
        [DS3LocationData(f"Large Soul of a Crestfallen Knight ${i + 1}", "Large Soul of a Crestfallen Knight", DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(3)] +

        # Gems
        [DS3LocationData(f"Dark Gem ${i + 1}",                           "Dark Gem",                           DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Blood Gem ${i + 1}",                          "Blood Gem",                          DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(1)] +
        [DS3LocationData(f"Blessed Gem ${i + 1}",                        "Blessed Gem",                        DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)] +
        [DS3LocationData(f"Hollow Gem ${i + 1}",                         "Hollow Gem",                         DS3LocationCategory.PROGRESSIVE_ITEM) for i in range(2)],

    "Progressive Items Health": [] +
        # Healing
        [DS3LocationData(f"Estus Shard #{i + 1}",       "Estus Shard",       DS3LocationCategory.HEALTH) for i in range(11)] +
        [DS3LocationData(f"Undead Bone Shard #{i + 1}", "Undead Bone Shard", DS3LocationCategory.HEALTH) for i in range(10)],
}

location_dictionary: Dict[str, DS3LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
