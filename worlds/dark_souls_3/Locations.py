from enum import IntEnum
from typing import Optional, Dict, List, Set
from dataclasses import dataclass

from BaseClasses import Location, LocationProgressType, Region


class DS3LocationCategory(IntEnum):
    WEAPON = 0
    SHIELD = 1
    ARMOR = 2
    RING = 3
    SPELL = 4
    KEY = 5
    BOSS = 6
    MISC = 7
    HEALTH = 8
    EVENT = 9

    UPGRADE = 10
    """The original location of any upgrade material.

    This includes various forms of titanite as well as infusion gems and Shriving Stones.
    """

    UNIQUE = 11
    """The original location of a unique item that's not a key, equipment, spell, or boss soul.

    This includes spellbooks, covenants, multiplayer items, coals, and various quest items.
    """


@dataclass
class DS3LocationData:
    name: str
    """The name of this location according to Archipelago.
    
    This needs to be unique within this world."""

    default_item_name: str
    """The name of the item that appears by default in this location."""

    category: DS3LocationCategory
    """The category into which this location falls."""

    offline: Optional[str] = None
    """The key in the offline randomizer's Slots table that corresponds to this location.

    By default, the offline randomizer chooses its location based on the region and the item name.
    If the item name is unique across the whole game, it can also look it up based on that alone. If
    there are multiple instances of the same item type in the same region, it will assume its order
    (in annotations.txt) matches Archipelago's order.

    In cases where this heuristic doesn't work, such as when Archipelago's region categorization or
    item name disagrees with the offline randomizer's, this field is used to provide an explicit
    association instead.
    """
 
    missable: bool = False
    """Whether this item is possible to permanently lose access to.

    This is also used for items that are *technically* possible to get at any time, but are
    prohibitively difficult without blocking off other checks (items dropped by NPCs on death
    generally fall into this category).

    Missable locations are always marked as excluded, so they will never contain
    progression or useful items.
    """

    dlc: bool = False
    """Whether this location is only accessible if the DLC is enabled."""

    # TODO: implement this properly
    ngp: bool = False
    """Whether this location only contains an item in NG+ and later.

    By default, these items aren't randomized or included in the randomization pool, but an option
    can be set to enable them even for NG runs."""

    npc: bool = False
    """Whether this item is contingent on killing an NPC or following their quest."""

    prominent: bool = False
    """Whether this is one of few particularly prominent places for items to appear.

    This is a small number of locations (boss drops and progression locations)
    intended to be set as priority locations for players who don't want a lot of
    mandatory checks.

    For bosses with multiple drops, only one should be marked prominent.
    """

    progression: bool = False
    """Whether this location normally contains an item that blocks forward progress."""

    boss: bool = False
    """Whether this location is a reward for defeating a full boss."""

    miniboss: bool = False
    """Whether this location is a reward for defeating a miniboss.

    The classification of "miniboss" is a bit fuzzy, but we consider them to be enemies that are
    visually distinctive in their locations, usually bigger than normal enemies, with a guaranteed
    item drop. NPCs are never considered minibosses, and some normal-looking enemies with guaranteed
    drops aren't either (these are instead classified as hidden locations)."""

    mimic: bool = False
    """Whether this location is dropped by a mimic."""

    hostile_npc: bool = False
    """Whether this location is dropped by a hostile NPC.

    An "NPC" is specifically a human (or rather, ash) is built like a player character rather than a
    monster. This includes both scripted invaders and NPCs who are always on the overworld. It does
    not include initially-friendly NPCs who become hostile as part of a quest or because you attack
    them.
    """

    lizard: bool = False
    """Whether this location is dropped by a (small) Crystal Lizard."""

    shop: bool = False
    """Whether this location appears in an NPC's shop."""

    key: bool = False
    """Whether this location normally contains a key.

    This is a literal key, not just a key item or a progression item.
    """

    hidden: bool = False
    """Whether this location is particularly tricky to find.

    This is for players without an encyclopedic knowledge of DS3 who don't want to get stuck looking
    for an illusory wall or one random mob with a guaranteed drop.
    """

    def location_groups(self) -> List[str]:
        """The names of location groups this location should appear in.

        This is computed from the properties assigned to this location."""
        names = []
        if self.prominent: names.append("Prominent")
        if self.progression: names.append("Progression")
        if self.boss: names.append("Boss Rewards")
        if self.miniboss: names.append("Miniboss Rewards")
        if self.mimic: names.append("Mimic Rewards")
        if self.hostile_npc: names.append("Hostile NPC Rewards")
        if self.lizard: names.append("Small Crystal Lizards")
        if self.key: names.append("Keys")
        if self.category == DS3LocationCategory.UPGRADE: names.append("Upgrade")
        if self.category == DS3LocationCategory.MISC: names.append("Miscellaneous")
        if self.hidden: names.append("Hidden")
        return names


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"
    category: DS3LocationCategory
    default_item_name: str
    offline: Optional[str] = None

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
    def from_data(
            player: int,
            data: DS3LocationData,
            address: Optional[int] = None,
            parent: Optional[Region] = None) -> "DarkSouls3Location":
        location = DarkSouls3Location(
            player,
            data.name,
            data.category,
            data.default_item_name,
            address,
            parent
        )
        location.offline = data.offline
        if data.missable:
            location.progress_type = LocationProgressType.EXCLUDED
        return location
        

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 150

        table_order = [
            "Cemetery of Ash",
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
            "Kiln of the First Flame",

            "Painted World of Ariandel (Before Contraption)",
            "Painted World of Ariandel (After Contraption)",
            "Dreg Heap",
            "Ringed City",

            "Greirat's Shop",
            "Karla's Shop",
        ]

        if len(location_tables) != len(table_order):
            for location in location_tables.keys():
                if location not in table_order:
                    raise Exception("Location table is missing location {}".format(location))
            for location in table_order:
                if location not in location_tables:
                    raise Exception("Table order is missing location {}".format(location))

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("The location table for {} has {} entries, that is more than {} entries".format(
                    region_name,
                    len(location_tables[region_name]),
                    table_offset,
                ))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output


location_tables = {
    "Cemetery of Ash": [
        DS3LocationData("CA: Soul of a Deserted Corpse",           "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("CA: Firebomb",                            "Firebomb x5",                       DS3LocationCategory.MISC),
        DS3LocationData("CA: Titanite Shard",                      "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("CA: Soul of an Unknown Traveler",         "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("CA: Speckled Stoneplate Ring+1",          "Speckled Stoneplate Ring+1",        DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CA: Titanite Scale",                      "Titanite Scale",                    DS3LocationCategory.UPGRADE,
                        miniboss = True),
    ],
    "Firelink Shrine": [
        DS3LocationData("FS: Skull Ring",                          "Skull Ring",                        DS3LocationCategory.RING,
                        hidden = True, npc = True), # Ludleth drop, does not permanently die
        DS3LocationData("FS: Uchigatana",                          "Uchigatana",                        DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Sword Master drop
        DS3LocationData("FS: Master's Attire",                     "Master's Attire",                   DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Sword Master drop
        DS3LocationData("FS: Master's Gloves",                     "Master's Gloves",                   DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Sword Master drop
        DS3LocationData("FS: Broken Straight Sword",               "Broken Straight Sword",             DS3LocationCategory.WEAPON),
        DS3LocationData("FS: Homeward Bone #1",                    "Homeward Bone",                     DS3LocationCategory.MISC),
        DS3LocationData("FS: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FS: Soul of a Deserted Corpse",           "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("FS: East-West Shield",                    "East-West Shield",                  DS3LocationCategory.SHIELD),
        DS3LocationData("FS: Homeward Bone #2",                    "Homeward Bone",                     DS3LocationCategory.MISC),
        DS3LocationData("FS: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FS: Wolf Ring+2",                         "Wolf Ring+2",                       DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("FS: Cracked Red Eye Orb",                 "Cracked Red Eye Orb x5",            DS3LocationCategory.UNIQUE,
                        missable = True, npc = True), # Leonhard (quest)
        DS3LocationData("FS: Lift Chamber Key",                    "Lift Chamber Key",                  DS3LocationCategory.KEY,
                        progression = True, npc = True, key = True), # Leonhard (kill or quest)

        # Shrine Handmaid shop
        DS3LocationData("FS: White Sign Soapstone",                "White Sign Soapstone",              DS3LocationCategory.UNIQUE,
                        shop = True),
        DS3LocationData("FS: Dried Finger",                        "Dried Finger",                      DS3LocationCategory.UNIQUE,
                        shop = True),
        DS3LocationData("FS: Tower Key",                           "Tower Key",                         DS3LocationCategory.KEY,
                        progression = True, shop = True, key = True),
        DS3LocationData("FS: Ember (Handmaid)",                    "Ember",                             DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000:', shop = True),
        DS3LocationData("FS: Farron Dart",                         "Farron Dart",                       DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000:', shop = True),
        DS3LocationData("FS: Soul Arrow",                          "Soul Arrow",                        DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000:', shop = True),
        DS3LocationData("FS: Heal Aid",                            "Heal Aid",                          DS3LocationCategory.SPELL,
                        shop = True),
        # Mortician's Ashes
        DS3LocationData("FS: Alluring Skull",                      "Alluring Skull",                    DS3LocationCategory.MISC,
                        shop = True),
        DS3LocationData("FS: Ember (Mortician)"  ,                 "Ember",                             DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,70000100:', shop = True),
        DS3LocationData("FS: Grave Key",                           "Grave Key",                         DS3LocationCategory.KEY,
                        shop = True, key = True),
        # Dreamchaser's Ashes
        DS3LocationData("FS: Life Ring",                           "Life Ring",                         DS3LocationCategory.RING,
                        shop = True),
        DS3LocationData("FS: Hidden Blessing #2",                  "Hidden Blessing",                   DS3LocationCategory.MISC,
                        missable = True, shop = True), # only if you say where the ashes were found
        # Paladin's Ashes
        DS3LocationData("FS: Lloyd's Shield Ring",                 "Lloyd's Shield Ring",               DS3LocationCategory.RING,
                        shop = True),
        # Grave Warden's Ashes
        DS3LocationData("FS: Ember (Grave Warden)",                "Ember",                             DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,70000103:', shop = True),
        # Prisoner Chief's Ashes
        DS3LocationData("FS: Karla's Pointed Hat",                 "Karla's Pointed Hat",               DS3LocationCategory.ARMOR,
                        offline = '99,0:-1:110000,70000105:', shop = True),
        DS3LocationData("FS: Karla's Coat",                        "Karla's Coat",                      DS3LocationCategory.ARMOR,
                        offline = '99,0:-1:110000,70000105:', shop = True),
        DS3LocationData("FS: Karla's Gloves",                      "Karla's Gloves",                    DS3LocationCategory.ARMOR,
                        offline = '99,0:-1:110000,70000105:', shop = True),
        DS3LocationData("FS: Karla's Trousers",                    "Karla's Trousers",                  DS3LocationCategory.ARMOR,
                        offline = '99,0:-1:110000,70000105:', shop = True),
        # Xanthous Ashes
        DS3LocationData("FS: Xanthous Overcoat",                   "Xanthous Overcoat",                 DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Xanthous Gloves",                     "Xanthous Gloves",                   DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Xanthous Trousers",                   "Xanthous Trousers",                 DS3LocationCategory.ARMOR,
                        shop = True),
        # Dragon Chaser's Ashes
        DS3LocationData("FS: Ember (Dragon Chaser)",               "Ember",                             DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,70000108:', shop = True),
        # Easterner's Ashes
        DS3LocationData("FS: Washing Pole",                        "Washing Pole",                      DS3LocationCategory.WEAPON,
                        shop = True),
        DS3LocationData("FS: Eastern Helm",                        "Eastern Helm",                      DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Eastern Armor",                       "Eastern Armor",                     DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Eastern Gauntlets",                   "Eastern Gauntlets",                 DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Eastern Leggings",                    "Eastern Leggings",                  DS3LocationCategory.ARMOR,
                        shop = True),
        DS3LocationData("FS: Wood Grain Ring",                     "Wood Grain Ring",                   DS3LocationCategory.RING,
                        shop = True),
        # Captain's Ashes
        DS3LocationData("FS: Millwood Knight Helm",                "Millwood Knight Helm",              DS3LocationCategory.ARMOR,
                        dlc = True, shop = True),
        DS3LocationData("FS: Millwood Knight Armor",               "Millwood Knight Armor",             DS3LocationCategory.ARMOR,
                        dlc = True, shop = True),
        DS3LocationData("FS: Millwood Knight Gauntlets",           "Millwood Knight Gauntlets",         DS3LocationCategory.ARMOR,
                        dlc = True, shop = True),
        DS3LocationData("FS: Millwood Knight Leggings",            "Millwood Knight Leggings",          DS3LocationCategory.ARMOR,
                        dlc = True, shop = True),
        DS3LocationData("FS: Refined Gem",                         "Refined Gem",                       DS3LocationCategory.UPGRADE,
                        dlc = True, shop = True),
    ],
    "Firelink Shrine Bell Tower": [
        # Guarded by Tower Key
        DS3LocationData("FSBT: Homeward Bone",                     "Homeward Bone x3",                  DS3LocationCategory.MISC),
        DS3LocationData("FSBT: Estus Ring",                        "Estus Ring",                        DS3LocationCategory.RING),
        DS3LocationData("FSBT: Estus Shard",                       "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("FSBT: Fire Keeper Soul",                  "Fire Keeper Soul",                  DS3LocationCategory.UNIQUE),
        DS3LocationData("FSBT: Fire Keeper Robe",                  "Fire Keeper Robe",                  DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Fire Keeper Gloves",                "Fire Keeper Gloves",                DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Fire Keeper Skirt",                 "Fire Keeper Skirt",                 DS3LocationCategory.ARMOR),
        DS3LocationData("FSBT: Covetous Silver Serpent Ring",      "Covetous Silver Serpent Ring",      DS3LocationCategory.RING,
                        hidden = True), # Behind illusory wall
        DS3LocationData("FSBT: Twinkling Titanite #1",             "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),

        # Mark all crow trades as missable since no one wants to have to try trading everything just
        # in case it gives a progression item.
        DS3LocationData("FSBT: Iron Bracelets",                    "Iron Bracelets",                    DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("FSBT: Ring of Sacrifice",                 "Ring of Sacrifice",                 DS3LocationCategory.MISC,
                        missable = True),
        DS3LocationData("FSBT: Porcine Shield",                    "Porcine Shield",                    DS3LocationCategory.SHIELD,
                        missable = True),
        DS3LocationData("FSBT: Lucatiel's Mask",                   "Lucatiel's Mask",                   DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("FSBT: Very good! Carving",                "Very good! Carving",                DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("FSBT: Thank you Carving",                 "Thank you Carving",                 DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("FSBT: I'm sorry Carving",                 "I'm sorry Carving",                 DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("FSBT: Sunlight Shield",                   "Sunlight Shield",                   DS3LocationCategory.SHIELD,
                        missable = True),
        DS3LocationData("FSBT: Hollow Gem",                        "Hollow Gem",                        DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Titanite Scale #1",                 "Titanite Scale x3",                 DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Help me! Carving",                  "Help me! Carving",                  DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("FSBT: Titanite Slab",                     "Titanite Slab",                     DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Hello Carving",                     "Hello Carving",                     DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("FSBT: Armor of the Sun",                  "Armor of the Sun",                  DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("FSBT: Large Titanite Shard",              "Large Titanite Shard",              DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Titanite Chunk",                    "Titanite Chunk",                    DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Iron Helm",                         "Iron Helm",                         DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("FSBT: Twinkling Titanite #2",             "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Iron Leggings",                     "Iron Leggings",                     DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("FSBT: Lightning Gem",                     "Lightning Gem",                     DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Twinkling Titanite #3",             "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Blessed Gem",                       "Blessed Gem",                       DS3LocationCategory.UPGRADE,
                        missable = True),
        DS3LocationData("FSBT: Titanite Scale #2",                 "Titanite Scale",                    DS3LocationCategory.UPGRADE,
                        missable = True),
    ],
    "High Wall of Lothric": [
        DS3LocationData("HWL: Soul of Boreal Valley Vordt",        "Soul of Boreal Valley Vordt",       DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("HWL: Soul of the Dancer",                 "Soul of the Dancer",                DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("HWL: Basin of Vows",                      "Basin of Vows",                     DS3LocationCategory.KEY,
                        prominent = True, progression = True),
        DS3LocationData("HWL: Small Lothric Banner",               "Small Lothric Banner",              DS3LocationCategory.KEY,
                        prominent = True, progression = True),
        DS3LocationData("HWL: Green Blossom #1",                   "Green Blossom x2",                  DS3LocationCategory.MISC,
                        hidden = True), # Down an obscured hallway
        DS3LocationData("HWL: Gold Pine Resin",                    "Gold Pine Resin x2",                DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("HWL: Large Soul of a Deserted Corpse #1", "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #1",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Standard Arrow",                     "Standard Arrow x12",                DS3LocationCategory.MISC),
        DS3LocationData("HWL: Longbow",                            "Longbow",                           DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Firebomb #1",                        "Firebomb x3",                       DS3LocationCategory.MISC),
        DS3LocationData("HWL: Throwing Knife #1",                  "Throwing Knife x8",                 DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #2",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Club",                               "Club",                              DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Claymore",                           "Claymore",                          DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Ember #1",                           "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("HWL: Firebomb #2",                        "Firebomb x2",                       DS3LocationCategory.MISC,
                        hidden = True), # In crates and furniture
        DS3LocationData("HWL: Titanite Shard #1",                  "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("HWL: Undead Hunter Charm",                "Undead Hunter Charm x2",            DS3LocationCategory.MISC,
                        hidden = True), # In a pot
        DS3LocationData("HWL: Firebomb #3",                        "Firebomb x3",                       DS3LocationCategory.MISC),
        DS3LocationData("HWL: Cell Key",                           "Cell Key",                          DS3LocationCategory.KEY,
                        key = True),
        DS3LocationData("HWL: Ember #2",                           "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #3",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Lucerne",                            "Lucerne",                           DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Mail Breaker",                       "Mail Breaker",                      DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Titanite Shard #2",                  "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("HWL: Rapier",                             "Rapier",                            DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Titanite Shard #3",                  "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("HWL: Large Soul of a Deserted Corpse #2", "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("HWL: Black Firebomb",                     "Black Firebomb x3",                 DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #4",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Ember #3",                           "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("HWL: Large Soul of a Deserted Corpse #3", "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC,
                        hidden = True), # Easily missed turnoff
        DS3LocationData("HWL: Binoculars",                         "Binoculars",                        DS3LocationCategory.UNIQUE),
        DS3LocationData("HWL: Ring of Sacrifice",                  "Ring of Sacrifice",                 DS3LocationCategory.MISC,
                        hidden = True), # Easily missed turnoff
        DS3LocationData("HWL: Throwing Knife #2",                  "Throwing Knife x6",                 DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #5",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Green Blossom #2",                   "Green Blossom x3",                  DS3LocationCategory.MISC),
        DS3LocationData("HWL: Broadsword",                         "Broadsword",                        DS3LocationCategory.WEAPON),
        DS3LocationData("HWL: Soul of a Deserted Corpse #6",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Firebomb #4",                        "Firebomb x3",                       DS3LocationCategory.MISC),
        DS3LocationData("HWL: Soul of a Deserted Corpse #7",       "Soul of a Deserted Corpse",         DS3LocationCategory.MISC),
        DS3LocationData("HWL: Estus Shard",                        "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("HWL: Fleshbite Ring+1",                   "Fleshbite Ring+1",                  DS3LocationCategory.RING,
                        hidden = True, ngp = True), # Hidden jump
        DS3LocationData("HWL: Ring of the Evil Eye+2",             "Ring of the Evil Eye+2",            DS3LocationCategory.RING,
                        hidden = True, ngp = True), # In barrels
        DS3LocationData("HWL: Silver Eagle Kite Shield",           "Silver Eagle Kite Shield",          DS3LocationCategory.SHIELD),
        DS3LocationData("HWL: Astora Straight Sword",              "Astora Straight Sword",             DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("HWL: Battle Axe",                         "Battle Axe",                        DS3LocationCategory.WEAPON,
                        offline = '01,0:53000960::', mimic = True),
        DS3LocationData("HWL: Ember #4",                           "Ember",                             DS3LocationCategory.MISC,
                        hidden = True, miniboss = True), # Only dropped by Pus of Man after transformation
        DS3LocationData("HWL: Titanite Shard #4",                  "Titanite Shard",                    DS3LocationCategory.UPGRADE,
                        hidden = True, miniboss = True), # Only dropped by Pus of Man after transformation
        DS3LocationData("HWL: Ember #5",                           "Ember",                             DS3LocationCategory.MISC,
                        hidden = True, miniboss = True), # Only dropped by Pus of Man after transformation
        DS3LocationData("HWL: Titanite Shard #5",                  "Titanite Shard",                    DS3LocationCategory.MISC,
                        hidden = True, miniboss = True), # Only dropped by Pus of Man after transformation
        DS3LocationData("HWL: Large Titanite Shard",               "Large Titanite Shard",              DS3LocationCategory.UPGRADE,
                        missable = True), # Getting fire-breathing wyvern down to 20% HP. Missable
                                          # because it requires range and is a crazy thing to do
        DS3LocationData("HWL: Refined Gem",                        "Refined Gem",                       DS3LocationCategory.UPGRADE,
                        miniboss = True), # Red-Eyed Lothric Knight drop
        DS3LocationData("HWL: Way of Blue",                        "Way of Blue",                       DS3LocationCategory.UNIQUE),
        DS3LocationData("HWL: Raw Gem",                            "Raw Gem",                           DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("HWL: Red Eye Orb",                        "Red Eye Orb",                       DS3LocationCategory.MISC,
                        miniboss = True),
        DS3LocationData("HWL: Vordt's Great Hammer",               "Vordt's Great Hammer",              DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("HWL: Pontiff's Left Eye",                 "Pontiff's Left Eye",                DS3LocationCategory.RING,
                        missable = True, boss = True, shop = True),
    ],
    "Undead Settlement": [
        DS3LocationData("US: Soul of the Rotted Greatwood",        "Soul of the Rotted Greatwood",      DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("US: Transposing Kiln",                    "Transposing Kiln",                  DS3LocationCategory.UNIQUE,
                        boss = True),
        DS3LocationData("US: Pyromancy Flame",                     "Pyromancy Flame",                   DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("US: Old Sage's Blindfold",                "Old Sage's Blindfold",              DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("US: Cornyx's Garb",                       "Cornyx's Garb",                     DS3LocationCategory.ARMOR,
                        offline = '02,0:50006141::', missable = True, npc = True),
        DS3LocationData("US: Cornyx's Wrap",                       "Cornyx's Wrap",                     DS3LocationCategory.ARMOR,
                        offline = '02,0:50006141::', missable = True, npc = True),
        DS3LocationData("US: Cornyx's Skirt",                      "Cornyx's Skirt",                    DS3LocationCategory.ARMOR,
                        offline = '02,0:50006141::', missable = True, npc = True),
        DS3LocationData("US: Tower Key",                           "Tower Key",                         DS3LocationCategory.KEY,
                        missable = True, npc = True, key = True),
        DS3LocationData("US: Hawk Ring",                           "Hawk Ring",                         DS3LocationCategory.RING,
                        npc = True), # Giant archer (kill or quest)
        DS3LocationData("US: Flynn's Ring",                        "Flynn's Ring",                      DS3LocationCategory.RING),
        DS3LocationData("US: Undead Bone Shard",                   "Undead Bone Shard",                 DS3LocationCategory.HEALTH),
        DS3LocationData("US: Alluring Skull #1",                   "Alluring Skull x2",                 DS3LocationCategory.MISC),
        DS3LocationData("US: Mortician's Ashes",                   "Mortician's Ashes",                 DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("US: Homeward Bone #1",                    "Homeward Bone x2",                  DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("US: Caduceus Round Shield",               "Caduceus Round Shield",             DS3LocationCategory.SHIELD),
        DS3LocationData("US: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("US: Soul of an Unknown Traveler #1",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("US: Repair Powder",                       "Repair Powder x2",                  DS3LocationCategory.MISC),
        DS3LocationData("US: Homeward Bone #2",                    "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("US: Titanite Shard #1",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("US: Wargod Wooden Shield",                "Wargod Wooden Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("US: Large Soul of a Deserted Corpse #1",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("US: Large Soul of a Deserted Corpse #2",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Titanite Shard #2",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("US: Alluring Skull #2",                   "Alluring Skull x2",                 DS3LocationCategory.MISC),
        DS3LocationData("US: Charcoal Pine Bundle #1",             "Charcoal Pine Bundle x2",           DS3LocationCategory.MISC),
        DS3LocationData("US: Blue Wooden Shield",                  "Blue Wooden Shield",                DS3LocationCategory.SHIELD),
        DS3LocationData("US: Cleric Hat",                          "Cleric Hat",                        DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Blue Robe",                    "Cleric Blue Robe",                  DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Gloves",                       "Cleric Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("US: Cleric Trousers",                     "Cleric Trousers",                   DS3LocationCategory.ARMOR),
        DS3LocationData("US: Soul of an Unknown Traveler #2",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("US: Charcoal Pine Resin",                 "Charcoal Pine Resin x2",            DS3LocationCategory.MISC),
        DS3LocationData("US: Loincloth",                           "Loincloth",                         DS3LocationCategory.ARMOR),
        DS3LocationData("US: Bloodbite Ring",                      "Bloodbite Ring",                    DS3LocationCategory.RING,
                        miniboss = True), # Giant Rat drop
        DS3LocationData("US: Charcoal Pine Bundle #2",             "Charcoal Pine Bundle x2",           DS3LocationCategory.MISC),
        DS3LocationData("US: Soul of an Unknown Traveler #3",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC,
                        hidden = True), # In crates
        DS3LocationData("US: Titanite Shard #3",                   "Titanite Shard",                    DS3LocationCategory.MISC),
        DS3LocationData("US: Red Hilted Halberd",                  "Red Hilted Halberd",                DS3LocationCategory.WEAPON),
        DS3LocationData("US: Rusted Coin",                         "Rusted Coin x2",                    DS3LocationCategory.MISC),
        DS3LocationData("US: Caestus",                             "Caestus",                           DS3LocationCategory.WEAPON),
        DS3LocationData("US: Saint's Talisman",                    "Saint's Talisman",                  DS3LocationCategory.WEAPON),
        DS3LocationData("US: Alluring Skull #3",                   "Alluring Skull x3",                 DS3LocationCategory.MISC),
        DS3LocationData("US: Large Club",                          "Large Club",                        DS3LocationCategory.WEAPON),
        DS3LocationData("US: Titanite Shard #4",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("US: Titanite Shard #5",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("US: Fading Soul #1",                      "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("US: Titanite Shard #6",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE,
                        hidden = True), # hidden fall
        DS3LocationData("US: Hand Axe",                            "Hand Axe",                          DS3LocationCategory.WEAPON),
        DS3LocationData("US: Soul of an Unknown Traveler #4",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("US: Ember #3",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("US: Mirrah Vest",                         "Mirrah Vest",                       DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("US: Mirrah Gloves",                       "Mirrah Gloves",                     DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("US: Mirrah Trousers",                     "Mirrah Trousers",                   DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("US: Plank Shield",                        "Plank Shield",                      DS3LocationCategory.SHIELD),
        DS3LocationData("US: Red Bug Pellet",                      "Red Bug Pellet x2",                 DS3LocationCategory.MISC),
        DS3LocationData("US: Chloranthy Ring",                     "Chloranthy Ring",                   DS3LocationCategory.RING,
                        hidden = True), # Hidden fall
        DS3LocationData("US: Fire Clutch Ring",                    "Fire Clutch Ring",                  DS3LocationCategory.RING),
        DS3LocationData("US: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("US: Firebomb",                            "Firebomb x6",                       DS3LocationCategory.MISC),
        DS3LocationData("US: Whip",                                "Whip",                              DS3LocationCategory.WEAPON,
                        hidden = True), # In enemy rando, the enemy may not burst through the wall
                                        # and make this room obvious
        DS3LocationData("US: Great Scythe",                        "Great Scythe",                      DS3LocationCategory.WEAPON),
        DS3LocationData("US: Homeward Bone #3",                    "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("US: Large Soul of a Deserted Corpse #3",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Ember #4",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("US: Large Soul of a Deserted Corpse #4",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Fading Soul #2",                      "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("US: Young White Branch #1",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("US: Ember #5",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("US: Large Soul of a Deserted Corpse #5",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Young White Branch #2",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("US: Reinforced Club",                     "Reinforced Club",                   DS3LocationCategory.WEAPON),
        DS3LocationData("US: Soul of a Nameless Soldier",          "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("US: Loretta's Bone",                      "Loretta's Bone",                    DS3LocationCategory.KEY),
        DS3LocationData("US: Northern Helm",                       "Northern Helm",                     DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Armor",                      "Northern Armor",                    DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Gloves",                     "Northern Gloves",                   DS3LocationCategory.ARMOR),
        DS3LocationData("US: Northern Trousers",                   "Northern Trousers",                 DS3LocationCategory.ARMOR),
        DS3LocationData("US: Partizan",                            "Partizan",                          DS3LocationCategory.WEAPON,
                        missable = True), # requires projectile
        DS3LocationData("US: Flame Stoneplate Ring",               "Flame Stoneplate Ring",             DS3LocationCategory.RING),
        DS3LocationData("US: Red and White Shield",                "Red and White Shield",              DS3LocationCategory.SHIELD,
                        offline = "02,0:53100740::"),
        DS3LocationData("US: Small Leather Shield",                "Small Leather Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("US: Pale Tongue",                         "Pale Tongue",                       DS3LocationCategory.MISC),
        DS3LocationData("US: Large Soul of a Deserted Corpse #6",  "Large Soul of a Deserted Corpse",   DS3LocationCategory.MISC),
        DS3LocationData("US: Kukri",                               "Kukri x9",                          DS3LocationCategory.MISC,
                        missable = True), # requires projectile
        DS3LocationData("US: Life Ring+1",                         "Life Ring+1",                       DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("US: Poisonbite Ring+1",                   "Poisonbite Ring+1",                 DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("US: Covetous Silver Serpent Ring+2",      "Covetous Silver Serpent Ring+2",    DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("US: Human Pine Resin",                    "Human Pine Resin x4",               DS3LocationCategory.MISC),
        DS3LocationData("US: Homeward Bone #4",                    "Homeward Bone",                     DS3LocationCategory.MISC),
        DS3LocationData("US: Irithyll Straight Sword",             "Irithyll Straight Sword",           DS3LocationCategory.WEAPON,
                        miniboss = True), # Boreal Outrider drop
        DS3LocationData("US: Fire Gem",                            "Fire Gem",                          DS3LocationCategory.UPGRADE,
                        miniboss = True), # Fire Demon drop
        DS3LocationData("US: Warrior of Sunlight",                 "Warrior of Sunlight",               DS3LocationCategory.UNIQUE,
                        hidden = True), # hidden fall
        DS3LocationData("US: Mound-makers",                        "Mound-makers",                      DS3LocationCategory.UNIQUE,
                        missable = True),
        DS3LocationData("US: Sharp Gem",                           "Sharp Gem",                         DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("US: Heavy Gem",                           "Heavy Gem",                         DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("US: Siegbräu",                            "Siegbräu",                          DS3LocationCategory.MISC,
                        missable = True, npc = True),
        DS3LocationData("US: Heavy Gem (Hawkwood)",                "Heavy Gem",                         DS3LocationCategory.UPGRADE,
                        offline = '00,0:50006070::', missable = True, npc = True), # Hawkwood (quest, after Greatwood or Sage)
        DS3LocationData("US: Hollowslayer Greatsword",             "Hollowslayer Greatsword",           DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("US: Arstor's Spear",                      "Arstor's Spear",                    DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Yoel/Yuria of Londor
        DS3LocationData("US: Soul Arrow",                          "Soul Arrow",                        DS3LocationCategory.SPELL,
                        offline = '99,0:-1:50000,110000,70000116:', missable = True, npc = True, shop = True),
        DS3LocationData("US: Heavy Soul Arrow",                    "Heavy Soul Arrow",                  DS3LocationCategory.SPELL,
                        offline = '99,0:-1:50000,110000,70000116:', missable = True, npc = True, shop = True),
        DS3LocationData("US: Magic Weapon",                        "Magic Weapon",                      DS3LocationCategory.SPELL,
                        offline = '99,0:-1:50000,110000,70000116:', missable = True, npc = True, shop = True),
        DS3LocationData("US: Magic Shield",                        "Magic Shield",                      DS3LocationCategory.SPELL,
                        offline = '99,0:-1:50000,110000,70000116:', missable = True, npc = True, shop = True),
        DS3LocationData("US: Soul Greatsword",                     "Soul Greatsword",                   DS3LocationCategory.SPELL,
                        offline = '99,0:-1:50000,110000,70000450,70000475:', missable = True, npc = True, shop = True),
        DS3LocationData("US: Dark Hand",                           "Dark Hand",                         DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("US: Untrue White Ring",                   "Untrue White Ring",                 DS3LocationCategory.RING,
                        missable = True, npc = True),
        DS3LocationData("US: Untrue Dark Ring",                    "Untrue Dark Ring",                  DS3LocationCategory.RING,
                        missable = True, npc = True),
        DS3LocationData("US: Londor Braille Divine Tome",          "Londor Braille Divine Tome",        DS3LocationCategory.UNIQUE,
                        offline = '99,0:-1:40000,110000,70000116:', missable = True, npc = True),
        DS3LocationData("US: Darkdrift",                           "Darkdrift",                         DS3LocationCategory.WEAPON,
                        missable = True, npc = True), # kill her or kill Soul of Cinder

        # Cornyx of the Great Swamp
        # These aren't missable because the Shrine Handmaid will carry them if you kill Cornyx.
        DS3LocationData("US: Fireball",                            "Fireball",                          DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Fire Surge",                          "Fire Surge",                        DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Great Combustion",                    "Great Combustion",                  DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Flash Sweat",                         "Flash Sweat",                       DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        # These are missable if you kill Cornyx before giving him the right tomes.
        DS3LocationData("US: Poison Mist",                         "Poison Mist",                       DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Fire Orb",                            "Fire Orb",                          DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Profuse Sweat",                       "Profuse Sweat",                     DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Bursting Fireball",                   "Bursting Fireball",                 DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Acid Surge",                          "Acid Surge",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Carthus Flame Arc",                   "Carthus Flame Arc",                 DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Carthus Beacon",                      "Carthus Beacon",                    DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Great Chaos Fire Orb",                "Great Chaos Fire Orb",              DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Chaos Storm",                         "Chaos Storm",                       DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),

        # Irina of Carim
        # These aren't in their own location because you don't actually need the Grave Key to access
        # Irena—you can just fall down the cliff near Eygon.
        DS3LocationData("US: Saint's Ring",                        "Saint's Ring",                      DS3LocationCategory.RING,
                        npc = True, shop = True),
        DS3LocationData("US: Heal",                                "Heal",                              DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Replenishment",                       "Replenishment",                     DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Caressing Tears",                     "Caressing Tears",                   DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Homeward",                            "Homeward",                          DS3LocationCategory.SPELL,
                        npc = True, shop = True),
        DS3LocationData("US: Med Heal",                            "Med Heal",                          DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Tears of Denial",                     "Tears of Denial",                   DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Force",                               "Force",                             DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Bountiful Light",                     "Bountiful Light",                   DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Magic Barrier",                       "Magic Barrier",                     DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Blessed Weapon",                      "Blessed Weapon",                    DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        # You can also get these from Karla
        DS3LocationData("US: Gnaw",                                "Gnaw",                              DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Deep Protection",                     "Deep Protection",                   DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Vow of Silence",                      "Vow of Silence",                    DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Dark Blade",                          "Dark Blade",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("US: Dead Again",                          "Dead Again",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
    ],
    "Road of Sacrifices": [
        DS3LocationData("RS: Soul of a Crystal Sage",              "Soul of a Crystal Sage",            DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("RS: Exile Greatsword",                    "Exile Greatsword",                  DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Exile Knight #2 drop
        DS3LocationData("RS: Great Club",                          "Great Club",                        DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Exile Knight #1 drop
        DS3LocationData("RS: Heysel Pick",                         "Heysel Pick",                       DS3LocationCategory.WEAPON,
                        missable = True, hostile_npc = True), # Heysel drop
        DS3LocationData("RS: Xanthous Crown",                      "Xanthous Crown",                    DS3LocationCategory.WEAPON,
                        missable = True, hostile_npc = True), # Heysel drop
        DS3LocationData("RS: Butcher Knife",                       "Butcher Knife",                     DS3LocationCategory.WEAPON,
                        hidden = True), # Guaranteed drop from a normal-looking Butcher
        DS3LocationData("RS: Titanite Shard #1",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("RS: Titanite Shard #2",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("RS: Green Blossom #1",                    "Green Blossom x4",                  DS3LocationCategory.MISC),
        DS3LocationData("RS: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("RS: Ring of Sacrifice",                   "Ring of Sacrifice",                 DS3LocationCategory.MISC,
                        hidden = True), # hidden fall
        DS3LocationData("RS: Soul of an Unknown Traveler #1",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("RS: Fallen Knight Helm",                  "Fallen Knight Helm",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Armor",                 "Fallen Knight Armor",               DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Gauntlets",             "Fallen Knight Gauntlets",           DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Fallen Knight Trousers",              "Fallen Knight Trousers",            DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Heretic's Staff",                     "Heretic's Staff",                   DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Large Soul of an Unknown Traveler",   "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("RS: Conjurator Hood",                     "Conjurator Hood",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Robe",                     "Conjurator Robe",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Manchettes",               "Conjurator Manchettes",             DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Conjurator Boots",                    "Conjurator Boots",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Soul of an Unknown Traveler #2",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("RS: Green Blossom #2",                    "Green Blossom x2",                  DS3LocationCategory.MISC),
        DS3LocationData("RS: Great Swamp Pyromancy Tome",          "Great Swamp Pyromancy Tome",        DS3LocationCategory.UNIQUE),
        DS3LocationData("RS: Homeward Bone",                       "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("RS: Titanite Shard #3",                   "Titanite Shard",                    DS3LocationCategory.MISC),
        DS3LocationData("RS: Twin Dragon Greatshield",             "Twin Dragon Greatshield",           DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Sorcerer Hood",                       "Sorcerer Hood",                     DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Sorcerer Robe",                       "Sorcerer Robe",                     DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Sorcerer Gloves",                     "Sorcerer Gloves",                   DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Sorcerer Trousers",                   "Sorcerer Trousers",                 DS3LocationCategory.ARMOR,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Sage Ring",                           "Sage Ring",                         DS3LocationCategory.RING,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Grass Crest Shield",                  "Grass Crest Shield",                DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("RS: Blue Bug Pellet",                     "Blue Bug Pellet x2",                DS3LocationCategory.MISC),
        DS3LocationData("RS: Soul of an Unknown Traveler #3",      "Soul of an Unknown Traveler",       DS3LocationCategory.MISC),
        DS3LocationData("RS: Shriving Stone",                      "Shriving Stone",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("RS: Titanite Shard #4",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("RS: Brigand Twindaggers",                 "Brigand Twindaggers",               DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Braille Divine Tome of Carim",        "Braille Divine Tome of Carim",      DS3LocationCategory.UNIQUE,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("RS: Sellsword Twinblades",                "Sellsword Twinblades",              DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Golden Falcon Shield",                "Golden Falcon Shield",              DS3LocationCategory.SHIELD),
        DS3LocationData("RS: Brigand Axe",                         "Brigand Axe",                       DS3LocationCategory.WEAPON),
        DS3LocationData("RS: Brigand Hood",                        "Brigand Hood",                      DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Armor",                       "Brigand Armor",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Gauntlets",                   "Brigand Gauntlets",                 DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Brigand Trousers",                    "Brigand Trousers",                  DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Morne's Ring",                        "Morne's Ring",                      DS3LocationCategory.RING,
                        hidden = True), # Hidden fall
        DS3LocationData("RS: Sellsword Helm",                      "Sellsword Helm",                    DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Armor",                     "Sellsword Armor",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Gauntlet",                  "Sellsword Gauntlet",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Sellsword Trousers",                  "Sellsword Trousers",                DS3LocationCategory.ARMOR),
        DS3LocationData("RS: Farron Coal",                         "Farron Coal",                       DS3LocationCategory.UNIQUE),
        DS3LocationData("RS: Chloranthy Ring+2",                   "Chloranthy Ring+2",                 DS3LocationCategory.RING,
                        hidden = True, ngp = True), # Hidden fall
        DS3LocationData("RS: Lingering Dragoncrest Ring+1",        "Lingering Dragoncrest Ring+1",      DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("RS: Great Swamp Ring",                    "Great Swamp Ring",                  DS3LocationCategory.RING,
                        miniboss = True), # Giant Crab drop
        DS3LocationData("RS: Blue Sentinels",                      "Blue Sentinels",                    DS3LocationCategory.UNIQUE,
                        missable = True, npc = True), # Horace quest
        DS3LocationData("RS: Crystal Gem",                         "Crystal Gem",                       DS3LocationCategory.UPGRADE),

        # Orbeck shop, all missable because he'll disappear if you don't talk to him for too long or
        # if you don't give him a scroll.
        DS3LocationData("RS: Farron Dart",                         "Farron Dart",                       DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True, shop = True),
        DS3LocationData("RS: Soul Arrow",                          "Soul Arrow",                        DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True, shop = True),
        DS3LocationData("RS: Great Soul Arrow",                    "Great Soul Arrow",                  DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Heavy Soul Arrow",                    "Heavy Soul Arrow",                  DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True, shop = True),
        DS3LocationData("RS: Great Heavy Soul Arrow",              "Great Heavy Soul Arrow",            DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Magic Weapon",                        "Magic Weapon",                      DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True, shop = True),
        DS3LocationData("RS: Magic Shield",                        "Magic Shield",                      DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True, shop = True),
        DS3LocationData("RS: Spook",                               "Spook",                             DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Aural Decoy",                         "Aural Decoy",                       DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Soul Greatsword",                     "Soul Greatsword",                   DS3LocationCategory.SPELL,
                        offline = '99,0:-1:110000,130100,70000111:', missable = True, npc = True),
        DS3LocationData("RS: Farron Flashsword",                   "Farron Flashsword",                 DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Pestilent Mist",                      "Pestilent Mist",                    DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Great Farron Dart",                   "Great Farron Dart",                 DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Farron Hail",                         "Farron Hail",                       DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Homing Soulmass",                     "Homing Soulmass",                   DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Soul Spear",                          "Soul Spear",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Homing Crystal Soulmass",             "Homing Crystal Soulmass",           DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Crystal Soul Spear",                  "Crystal Soul Spear",                DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Crystal Magic Weapon",                "Crystal Magic Weapon",              DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Cast Light",                          "Cast Light",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Twisted Wall of Light",               "Twisted Wall of Light",             DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Hidden Weapon",                       "Hidden Weapon",                     DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Hidden Body",                         "Hidden Body",                       DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Repair",                              "Repair",                            DS3LocationCategory.SPELL,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RS: Clandestine Coat",                    "Clandestine Coat",                  DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True), # Shrine Handmaid with Orbeck's Ashes + reload
        DS3LocationData("RS: Young Dragon Ring",                   "Young Dragon Ring",                 DS3LocationCategory.RING,
                        missable = True, npc = True),
        DS3LocationData("RS: Slumbering Dragoncrest Ring",         "Slumbering Dragoncrest Ring",       DS3LocationCategory.RING,
                        missable = True, npc = True),
        DS3LocationData("RS: Crystal Sage's Rapier",               "Crystal Sage's Rapier",             DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RS: Crystal Hail",                        "Crystal Hail",                      DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RS: Farron Greatsword",                   "Farron Greatsword",                 DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RS: Wolf Knight's Greatsword",            "Wolf Knight's Greatsword",          DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after killing Crystal Sage
        DS3LocationData("RS: Sage's Big Hat",                      "Sage's Big Hat",                    DS3LocationCategory.ARMOR,
                        boss = True, shop = True),

        # Yuria of Londor for Orbeck's Ashes
        DS3LocationData("RS: Morion Blade",                        "Morion Blade",                      DS3LocationCategory.WEAPON,
                        missable = True, npc = True),

        # Hawkwood after killing Abyss Watchers
        DS3LocationData("RS: Farron Ring",                         "Farron Ring",                       DS3LocationCategory.RING,
                        missable = True, npc = True),
    ],
    "Cathedral of the Deep": [
        DS3LocationData("CD: Herald Helm",                         "Herald Helm",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Herald Armor",                        "Herald Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Herald Gloves",                       "Herald Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Herald Trousers",                     "Herald Trousers",                   DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Twinkling Titanite #1",               "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CD: Twinkling Titanite #2",               "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CD: Small Doll",                          "Small Doll",                        DS3LocationCategory.KEY,
                        prominent = True, progression = True, boss = True),
        DS3LocationData("CD: Soul of the Deacons of the Deep",     "Soul of the Deacons of the Deep",   DS3LocationCategory.BOSS,
                        boss = True),
        DS3LocationData("CD: Black Eye Orb",                       "Black Eye Orb",                     DS3LocationCategory.UNIQUE,
                        missable = True, npc = True),
        DS3LocationData("CD: Winged Spear #1",                     "Winged Spear",                      DS3LocationCategory.WEAPON,
                        missable = True), # Patches (kill)
        DS3LocationData("CD: Spider Shield",                       "Spider Shield",                     DS3LocationCategory.SHIELD,
                        hostile_npc = True), # Brigand
        DS3LocationData("CD: Notched Whip",                        "Notched Whip",                      DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Titanite Shard #1",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("CD: Astora Greatsword",                   "Astora Greatsword",                 DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Executioner's Greatsword",            "Executioner's Greatsword",          DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Undead Bone Shard",                   "Undead Bone Shard",                 DS3LocationCategory.HEALTH),
        DS3LocationData("CD: Curse Ward Greatshield",              "Curse Ward Greatshield",            DS3LocationCategory.SHIELD),
        DS3LocationData("CD: Titanite Shard #2",                   "Titanite Shard",                    DS3LocationCategory.MISC),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #1", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CD: Paladin's Ashes",                     "Paladin's Ashes",                   DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("CD: Arbalest",                            "Arbalest",                          DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("CD: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CD: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CD: Poisonbite Ring",                     "Poisonbite Ring",                   DS3LocationCategory.RING),
        DS3LocationData("CD: Drang Armor",                         "Drang Armor",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Ember #3",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CD: Duel Charm #1",                       "Duel Charm x3",                     DS3LocationCategory.MISC),
        DS3LocationData("CD: Seek Guidance",                       "Seek Guidance",                     DS3LocationCategory.SPELL),
        DS3LocationData("CD: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("CD: Maiden Hood",                         "Maiden Hood",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Robe",                         "Maiden Robe",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Gloves",                       "Maiden Gloves",                     DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Maiden Skirt",                        "Maiden Skirt",                      DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Pale Tongue #1",                      "Pale Tongue",                       DS3LocationCategory.MISC,
                        hidden = True), # hidden fall
        DS3LocationData("CD: Fading Soul",                         "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("CD: Blessed Gem",                         "Blessed Gem",                       DS3LocationCategory.UPGRADE,
                        hidden = True), # hidden fall
        DS3LocationData("CD: Red Bug Pellet #1",                   "Red Bug Pellet",                    DS3LocationCategory.MISC),
        DS3LocationData("CD: Soul of a Nameless Soldier #1",       "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("CD: Duel Charm #2",                       "Duel Charm",                        DS3LocationCategory.MISC),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #2", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CD: Ember #4",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CD: Repair Powder",                       "Repair Powder x3",                  DS3LocationCategory.MISC),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #3", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #4", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CD: Undead Hunter Charm",                 "Undead Hunter Charm x3",            DS3LocationCategory.MISC,
                        hidden = True), # Have to jump from a buttress
        DS3LocationData("CD: Red Bug Pellet #2",                   "Red Bug Pellet x3",                 DS3LocationCategory.MISC),
        DS3LocationData("CD: Titanite Shard #3",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("CD: Titanite Shard #4",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("CD: Rusted Coin #1",                      "Rusted Coin x2",                    DS3LocationCategory.MISC),
        DS3LocationData("CD: Drang Hammers",                       "Drang Hammers",                     DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Drang Shoes",                         "Drang Shoes",                       DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #5", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CD: Pale Tongue #2",                      "Pale Tongue",                       DS3LocationCategory.MISC),
        DS3LocationData("CD: Drang Gauntlets",                     "Drang Gauntlets",                   DS3LocationCategory.ARMOR),
        DS3LocationData("CD: Soul of a Nameless Soldier #2",       "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("CD: Exploding Bolt",                      "Exploding Bolt x6",                 DS3LocationCategory.MISC),
        DS3LocationData("CD: Lloyd's Sword Ring",                  "Lloyd's Sword Ring",                DS3LocationCategory.RING),
        DS3LocationData("CD: Soul of a Nameless Soldier #3",       "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("CD: Homeward Bone",                       "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("CD: Deep Gem",                            "Deep Gem",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CD: Titanite Shard #5",                   "Titanite Shard",                    DS3LocationCategory.MISC),
        DS3LocationData("CD: Large Soul of an Unknown Traveler #6", "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        # Before the stairs leading down into the Deacons fight
        DS3LocationData("CD: Ring of the Evil Eye+1",              "Ring of the Evil Eye+1",            DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CD: Ring of Favor+2",                     "Ring of Favor+2",                   DS3LocationCategory.RING,
                        hidden = True, ngp = True), # Hidden fall
        DS3LocationData("CD: Crest Shield",                        "Crest Shield",                      DS3LocationCategory.SHIELD,
                        hidden = True), # Hidden fall
        DS3LocationData("CD: Young White Branch #1",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("CD: Young White Branch #2",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("CD: Saint-tree Bellvine",                 "Saint-tree Bellvine",               DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Saint Bident",                        "Saint Bident",                      DS3LocationCategory.WEAPON),
        DS3LocationData("CD: Archdeacon White Crown",              "Archdeacon White Crown",            DS3LocationCategory.ARMOR,
                        boss = True, hidden = True), # Have to return to a cleared area
        DS3LocationData("CD: Archdeacon Holy Garb",                "Archdeacon Holy Garb",              DS3LocationCategory.ARMOR,
                        boss = True, hidden = True), # Have to return to a cleared area
        DS3LocationData("CD: Archdeacon Skirt",                    "Archdeacon Skirt",                  DS3LocationCategory.ARMOR,
                        boss = True, hidden = True), # Have to return to a cleared area
        DS3LocationData("CD: Heysel Pick",                         "Heysel Pick",                       DS3LocationCategory.WEAPON,
                        missable = True),
        DS3LocationData("CD: Xanthous Crown",                      "Xanthous Crown",                    DS3LocationCategory.WEAPON,
                        missable = True),
        DS3LocationData("CD: Deep Ring",                           "Deep Ring",                         DS3LocationCategory.RING,
                        hidden = True), # Guaranteed drop from a normal-looking Deacon
        DS3LocationData("CD: Deep Braille Divine Tome",            "Deep Braille Divine Tome",          DS3LocationCategory.UNIQUE,
                        mimic = True),
        DS3LocationData("CD: Red Sign Soapstone",                  "Red Sign Soapstone",                DS3LocationCategory.UNIQUE,
                        hidden = True), # Guaranteed drop from a normal-looking Corpse-grub
        DS3LocationData("CD: Aldrich's Sapphire",                  "Aldrich's Sapphire",                DS3LocationCategory.RING,
                        miniboss = True), # Deep Accursed Drop
        DS3LocationData("CD: Dung Pie",                            "Dung Pie x4",                       DS3LocationCategory.MISC,
                        miniboss = True), # Giant Slave drop
        DS3LocationData("CD: Large Titanite Shard",                "Large Titanite Shard",              DS3LocationCategory.UPGRADE,
                        miniboss = True), # Giant Slave drop
        DS3LocationData("CD: Titanite Scale",                      "Titanite Scale",                    DS3LocationCategory.UPGRADE,
                        miniboss = True), # Ravenous Crystal Lizard drop
        DS3LocationData("CD: Twinkling Titanite #3",               "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CD: Twinkling Titanite #4",               "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CD: Rosaria's Fingers",                   "Rosaria's Fingers",                 DS3LocationCategory.UNIQUE,
                        hidden = True), # Hidden fall
        DS3LocationData("CD: Cleric's Candlestick",                "Cleric's Candlestick",              DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("CD: Deep Soul",                           "Deep Soul",                         DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Longfinger Kirk drops
        DS3LocationData("CD: Barbed Straight Sword",               "Barbed Straight Sword",             DS3LocationCategory.WEAPON,
                        missable = True, hostile_npc = True),
        DS3LocationData("CD: Spiked Shield",                       "Spiked Shield",                     DS3LocationCategory.SHIELD,
                        missable = True, hostile_npc = True),
        # In Rosaria's Bed Chamber
        DS3LocationData("CD: Helm of Thorns",                      "Helm of Thorns",                    DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("CD: Armor of Thorns",                     "Armor of Thorns",                   DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("CD: Gauntlets of Thorns",                 "Gauntlets of Thorns",               DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("CD: Leggings of Thorns",                  "Leggings of Thorns",                DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),

        # Unbreakable Patches
        DS3LocationData("CD: Rusted Coin #2",                      "Rusted Coin",                       DS3LocationCategory.MISC,
                        missable = True, npc = True),
        DS3LocationData("CD: Rusted Gold Coin",                    "Rusted Gold Coin",                  DS3LocationCategory.MISC,
                        offline = '99,0:50006201::', missable = True, npc = True), # Don't forgive Patches
        DS3LocationData("CD: Shotel",                              "Shotel",                            DS3LocationCategory.WEAPON,
                        missable = True, npc = True, shop = True),
        DS3LocationData("CD: Ember #5",                            "Ember",                             DS3LocationCategory.MISC,
                        missable = True, npc = True, shop = True),
        DS3LocationData("CD: Hidden Blessing",                     "Hidden Blessing",                   DS3LocationCategory.MISC,
                        missable = True, npc = True, shop = True),
        DS3LocationData("CD: Horsehoof Ring",                      "Horsehoof Ring",                    DS3LocationCategory.RING,
                        missable = True, npc = True, shop = True), # (kill or buy)
    ],
    "Farron Keep": [
        DS3LocationData("FK: Lightning Spear",                     "Lightning Spear",                   DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Dragon Crest Shield",                 "Dragon Crest Shield",               DS3LocationCategory.SHIELD),
        DS3LocationData("FK: Soul of the Blood of the Wolf",       "Soul of the Blood of the Wolf",     DS3LocationCategory.BOSS,
                        boss = True),
        DS3LocationData("FK: Cinders of a Lord - Abyss Watcher",   "Cinders of a Lord - Abyss Watcher", DS3LocationCategory.KEY,
                        offline = "03,0:50002100::", prominent = True, progression = True, boss = True),
        DS3LocationData("FK: Manikin Claws",                       "Manikin Claws",                     DS3LocationCategory.WEAPON,
                        missable = True, hostile_npc = True, npc = True), # Londor Pale Shade (if Yoel/Yuria hostile)
        DS3LocationData("FK: Purple Moss Clump #1",                "Purple Moss Clump x2",              DS3LocationCategory.MISC),
        DS3LocationData("FK: Purple Moss Clump #2",                "Purple Moss Clump x4",              DS3LocationCategory.MISC),
        DS3LocationData("FK: Greatsword",                          "Greatsword",                        DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Hollow Gem",                          "Hollow Gem",                        DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Fading Soul",                         "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("FK: Purple Moss Clump #3",                "Purple Moss Clump x3",              DS3LocationCategory.MISC),
        DS3LocationData("FK: Undead Bone Shard",                   "Undead Bone Shard",                 DS3LocationCategory.HEALTH),
        DS3LocationData("FK: Atonement",                           "Atonement",                         DS3LocationCategory.SPELL,
                        hidden = True), # Hidden fall
        DS3LocationData("FK: Titanite Shard #1",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Iron Flesh",                          "Iron Flesh",                        DS3LocationCategory.SPELL),
        DS3LocationData("FK: Stone Parma",                         "Stone Parma",                       DS3LocationCategory.SHIELD),
        DS3LocationData("FK: Rotten Pine Resin #1",                "Rotten Pine Resin x2",              DS3LocationCategory.MISC),
        DS3LocationData("FK: Titanite Shard #2",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Rusted Gold Coin",                    "Rusted Gold Coin",                  DS3LocationCategory.MISC,
                        hidden = True), # Hidden behind a wall
        DS3LocationData("FK: Nameless Knight Helm",                "Nameless Knight Helm",              DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Armor",               "Nameless Knight Armor",             DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Gauntlets",           "Nameless Knight Gauntlets",         DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Nameless Knight Leggings",            "Nameless Knight Leggings",          DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Shriving Stone",                      "Shriving Stone",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Repair Powder",                       "Repair Powder x4",                  DS3LocationCategory.MISC,
                        hidden = True), # Out-of-the-way hard-to-see cave
        DS3LocationData("FK: Golden Scroll",                       "Golden Scroll",                     DS3LocationCategory.UNIQUE,
                        hostile_npc = True), # Out-of-the-way hard-to-see cave
        DS3LocationData("FK: Sage's Scroll",                       "Sage's Scroll",                     DS3LocationCategory.UNIQUE),
        DS3LocationData("FK: Dreamchaser's Ashes",                 "Dreamchaser's Ashes",               DS3LocationCategory.KEY,
                        progression = True, hidden = True), # Behind illusory wall
        DS3LocationData("FK: Titanite Shard #3",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Wolf's Blood Swordgrass",             "Wolf's Blood Swordgrass",           DS3LocationCategory.MISC),
        DS3LocationData("FK: Great Magic Weapon",                  "Great Magic Weapon",                DS3LocationCategory.SPELL),
        DS3LocationData("FK: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FK: Titanite Shard #4",                   "Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Titanite Shard #5",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Titanite Shard #6",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Black Bug Pellet",                    "Black Bug Pellet x3",               DS3LocationCategory.MISC),
        DS3LocationData("FK: Rotten Pine Resin #2",                "Rotten Pine Resin x4",              DS3LocationCategory.MISC),
        DS3LocationData("FK: Poison Gem",                          "Poison Gem",                        DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Ragged Mask",                         "Ragged Mask",                       DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("FK: Homeward Bone",                       "Homeward Bone x2",                  DS3LocationCategory.HEALTH),
        DS3LocationData("FK: Titanite Shard #7",                   "Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Large Soul of a Nameless Soldier #1", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("FK: Prism Stone",                         "Prism Stone x10",                   DS3LocationCategory.MISC),
        DS3LocationData("FK: Large Soul of a Nameless Soldier #2", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("FK: Sage's Coal",                         "Sage's Coal",                       DS3LocationCategory.UNIQUE),
        DS3LocationData("FK: Gold Pine Bundle",                    "Gold Pine Bundle x6",               DS3LocationCategory.MISC),
        DS3LocationData("FK: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FK: Soul of a Nameless Soldier",          "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("FK: Large Soul of an Unknown Traveler",   "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("FK: Greataxe",                            "Greataxe",                          DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Ember #3",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FK: Ember #4",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("FK: Dark Stoneplate Ring+2",              "Dark Stoneplate Ring+2",            DS3LocationCategory.RING,
                        hidden = True, ngp = True), # Hidden behind wall
        DS3LocationData("FK: Magic Stoneplate Ring+1",             "Magic Stoneplate Ring+1",           DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("FK: Wolf Ring+1",                         "Wolf Ring+1",                       DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("FK: Antiquated Dress",                    "Antiquated Dress",                  DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Out-of-the-way hard-to-see cave
        DS3LocationData("FK: Antiquated Gloves",                   "Antiquated Gloves",                 DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Out-of-the-way hard-to-see cave
        DS3LocationData("FK: Antiquated Skirt",                    "Antiquated Skirt",                  DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Out-of-the-way hard-to-see cave
        DS3LocationData("FK: Sunlight Talisman",                   "Sunlight Talisman",                 DS3LocationCategory.WEAPON),
        DS3LocationData("FK: Young White Branch #1",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("FK: Young White Branch #2",               "Young White Branch",                DS3LocationCategory.MISC),
        DS3LocationData("FK: Crown of Dusk",                       "Crown of Dusk",                     DS3LocationCategory.ARMOR),
        DS3LocationData("FK: Lingering Dragoncrest Ring",          "Lingering Dragoncrest Ring",        DS3LocationCategory.RING,
                        miniboss = True), # Great Crab drop
        DS3LocationData("FK: Pharis's Hat",                        "Pharis's Hat",                      DS3LocationCategory.ARMOR,
                        hidden = True), # Guaranteed drop from a normal-looking Elder Ghru
        DS3LocationData("FK: Black Bow of Pharis",                 "Black Bow of Pharis",               DS3LocationCategory.WEAPON,
                        hidden = True), # Guaranteed drop from a normal-looking Elder Ghru
        DS3LocationData("FK: Titanite Scale",                      "Titanite Scale x2",                 DS3LocationCategory.UPGRADE,
                        miniboss = True), # Ravenous Crystal Lizard drop
        DS3LocationData("FK: Large Titanite Shard #1",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Large Titanite Shard #2",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("FK: Heavy Gem",                           "Heavy Gem",                         DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("FK: Twinkling Titanite",                  "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("FK: Soul of a Stray Demon",               "Soul of a Stray Demon",             DS3LocationCategory.BOSS,
                        miniboss = True),
        DS3LocationData("FK: Watchdogs of Farron",                 "Watchdogs of Farron",               DS3LocationCategory.UNIQUE),
        DS3LocationData("FK: Hawkwood's Shield",                   "Hawkwood's Shield",                 DS3LocationCategory.SHIELD,
                        missable = True, npc = True), # Hawkwood (quest, after Greatwood, Sage, Watchers, and Deacons)
        DS3LocationData("FK: Havel's Ring",                        "Havel's Ring",                      DS3LocationCategory.RING,
                        missable = True, boss = True, shop = True),
        DS3LocationData("FK: Boulder Heave",                       "Boulder Heave",                     DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after killing exiles
        DS3LocationData("FK: Exile Mask",                          "Exile Mask",                        DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("FK: Exile Armor",                         "Exile Armor",                       DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("FK: Exile Gauntlets",                     "Exile Gauntlets",                   DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("FK: Exile Leggings",                      "Exile Leggings",                    DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),

        # Shrine Handmaid after killing Abyss Watchers
        DS3LocationData("FK: Undead Legion Helm",                  "Undead Legion Helm",                DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("FK: Undead Legion Armor",                 "Undead Legion Armor",               DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("FK: Undead Legion Gauntlet",              "Undead Legion Gauntlet",            DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("FK: Undead Legion Leggings",              "Undead Legion Leggings",            DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
    ],
    "Catacombs of Carthus": [
        DS3LocationData("CC: Soul of High Lord Wolnir",            "Soul of High Lord Wolnir",          DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("CC: Carthus Rouge #1",                    "Carthus Rouge x2",                  DS3LocationCategory.MISC),
        DS3LocationData("CC: Sharp Gem",                           "Sharp Gem",                         DS3LocationCategory.UPGRADE),
        DS3LocationData("CC: Soul of a Nameless Soldier #1",       "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("CC: Titanite Shard #1",                   "Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("CC: Bloodred Moss Clump",                 "Bloodred Moss Clump x3",            DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Milkring",                    "Carthus Milkring",                  DS3LocationCategory.RING),
        DS3LocationData("CC: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Rouge #2",                    "Carthus Rouge x3",                  DS3LocationCategory.MISC),
        DS3LocationData("CC: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Bloodring",                   "Carthus Bloodring",                 DS3LocationCategory.RING),
        DS3LocationData("CC: Titanite Shard #2",                   "Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("CC: Titanite Shard #3",                   "Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("CC: Ember #3",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("CC: Carthus Pyromancy Tome",              "Carthus Pyromancy Tome",            DS3LocationCategory.UNIQUE,
                        hidden = True), # Behind illusory wall
        DS3LocationData("CC: Large Titanite Shard #1",             "Large Titanite Shard",              DS3LocationCategory.MISC),
        DS3LocationData("CC: Large Titanite Shard #2",             "Large Titanite Shard",              DS3LocationCategory.MISC),
        DS3LocationData("CC: Yellow Bug Pellet",                   "Yellow Bug Pellet x3",              DS3LocationCategory.MISC),
        DS3LocationData("CC: Large Soul of a Nameless Soldier #1", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("CC: Black Bug Pellet",                    "Black Bug Pellet x2",               DS3LocationCategory.MISC),
        DS3LocationData("CC: Grave Warden's Ashes",                "Grave Warden's Ashes",              DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("CC: Large Titanite Shard #3",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("CC: Large Soul of a Nameless Soldier #2", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("CC: Old Sage's Blindfold",                "Old Sage's Blindfold",              DS3LocationCategory.ARMOR),
        DS3LocationData("CC: Witch's Ring",                        "Witch's Ring",                      DS3LocationCategory.RING),
        DS3LocationData("CC: Soul of a Nameless Soldier #2",       "Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("CC: Grave Warden Pyromancy Tome",         "Grave Warden Pyromancy Tome",       DS3LocationCategory.UNIQUE),
        DS3LocationData("CC: Large Soul of an Unknown Traveler",   "Large Soul of an Unknown Traveler", DS3LocationCategory.MISC),
        DS3LocationData("CC: Ring of Steel Protection+2",          "Ring of Steel Protection+2",        DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CC: Thunder Stoneplate Ring+1",           "Thunder Stoneplate Ring+1",         DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CC: Undead Bone Shard",                   "Undead Bone Shard",                 DS3LocationCategory.HEALTH,
                        hidden = True), # Skeleton Ball puzzle
        DS3LocationData("CC: Dark Gem",                            "Dark Gem",                          DS3LocationCategory.UPGRADE,
                        hidden = True), # Skeleton Ball puzzle
        DS3LocationData("CC: Black Blade",                         "Black Blade",                       DS3LocationCategory.WEAPON,
                        mimic = True),
        DS3LocationData("CC: Soul of a Demon",                     "Soul of a Demon",                   DS3LocationCategory.BOSS,
                        miniboss = True),
        DS3LocationData("CC: Twinkling Titanite",                  "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CC: Fire Gem",                            "Fire Gem",                          DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("CC: Homeward Bone",                       "Homeward Bone",                     DS3LocationCategory.MISC),
        DS3LocationData("CC: Pontiff's Right Eye",                 "Pontiff's Right Eye",               DS3LocationCategory.RING,
                        miniboss = True), # Sullyvahn's Beast drop, in CC because it doesn't require Small Doll
        DS3LocationData("CC: Wolnir's Holy Sword",                 "Wolnir's Holy Sword",               DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("CC: Black Serpent",                       "Black Serpent",                     DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
        DS3LocationData("CC: Demon's Greataxe",                    "Demon's Greataxe",                  DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("CC: Demon's Fist",                        "Demon's Fist",                      DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after killing High Lord Wolnir
        DS3LocationData("CC: Wolnir's Crown",                      "Wolnir's Crown",                    DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
    ],
    "Smouldering Lake": [
        DS3LocationData("SL: Soul of the Old Demon King",          "Soul of the Old Demon King",        DS3LocationCategory.BOSS,
                        prominent = True, boss = True),

        DS3LocationData("SL: Fume Ultra Greatsword",               "Fume Ultra Greatsword",             DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Knight Slayer Tsorig drop
        DS3LocationData("SL: Black Iron Greatshield",              "Black Iron Greatshield",            DS3LocationCategory.SHIELD,
                        hostile_npc = True), # Knight Slayer Tsorig drop
        DS3LocationData("SL: Large Titanite Shard #1",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #2",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #3",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #4",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #5",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Yellow Bug Pellet",                   "Yellow Bug Pellet x2",              DS3LocationCategory.MISC),
        DS3LocationData("SL: Large Titanite Shard #6",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #7",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Large Titanite Shard #8",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Speckled Stoneplate Ring",            "Speckled Stoneplate Ring",          DS3LocationCategory.RING,
                        hidden = True), # Requires careful ballista shot
        DS3LocationData("SL: Homeward Bone",                       "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("SL: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("SL: Chaos Gem #1",                        "Chaos Gem",                         DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("SL: Izalith Pyromancy Tome",              "Izalith Pyromancy Tome",            DS3LocationCategory.UNIQUE),
        DS3LocationData("SL: Black Knight Sword",                  "Black Knight Sword",                DS3LocationCategory.WEAPON,
                        hidden = True), # Behind illusory wall
        DS3LocationData("SL: Ember #3",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("SL: Quelana Pyromancy Tome",              "Quelana Pyromancy Tome",            DS3LocationCategory.UNIQUE),
        DS3LocationData("SL: Izalith Staff",                       "Izalith Staff",                     DS3LocationCategory.WEAPON,
                        hidden = True), # Behind illusory wall
        DS3LocationData("SL: White Hair Talisman",                 "White Hair Talisman",               DS3LocationCategory.WEAPON,
                        missable = True), # In lava
        DS3LocationData("SL: Toxic Mist",                          "Toxic Mist",                        DS3LocationCategory.SPELL,
                        missable = True), # In lava
        DS3LocationData("SL: Undead Bone Shard #1",                "Undead Bone Shard",                 DS3LocationCategory.HEALTH),
        DS3LocationData("SL: Titanite Scale",                      "Titanite Scale",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("SL: Shield of Want",                      "Shield of Want",                    DS3LocationCategory.SHIELD),
        DS3LocationData("SL: Soul of a Crestfallen Knight",        "Soul of a Crestfallen Knight",      DS3LocationCategory.MISC),
        DS3LocationData("SL: Ember #4",                            "Ember",                             DS3LocationCategory.MISC,
                        missable = True), # In lava
        DS3LocationData("SL: Sacred Flame",                        "Sacred Flame",                      DS3LocationCategory.SPELL,
                        missable = True, hidden = True), # In lava
        DS3LocationData("SL: Dragonrider Bow",                     "Dragonrider Bow",                   DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("SL: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH,
                        hidden = True), # Behind illusory wall
        DS3LocationData("SL: Bloodbite Ring+1",                    "Bloodbite Ring+1",                  DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("SL: Flame Stoneplate Ring+2",             "Flame Stoneplate Ring+2",           DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Behind illusory wall
        DS3LocationData("SL: Large Titanite Shard #9",             "Large Titanite Shard x3",           DS3LocationCategory.UPGRADE,
                        hidden = True), # Behind illusory wall
        DS3LocationData("SL: Undead Bone Shard #2",                "Undead Bone Shard",                 DS3LocationCategory.HEALTH,
                        miniboss = True), # Sand Worm drop
        DS3LocationData("SL: Lightning Stake",                     "Lightning Stake",                   DS3LocationCategory.SPELL,
                        miniboss = True), # Sand Worm drop
        DS3LocationData("SL: Twinkling Titanite",                  "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("SL: Titanite Chunk",                      "Titanite Chunk",                    DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("SL: Chaos Gem #2",                        "Chaos Gem",                         DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("SL: Knight Slayer's Ring",                "Knight Slayer's Ring",              DS3LocationCategory.RING,
                        hostile_npc = True), # Knight Slayer Tsorig drop
        DS3LocationData("SL: Old King's Great Hammer",             "Old King's Great Hammer",           DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("SL: Chaos Bed Vestiges",                  "Chaos Bed Vestiges",                DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Horace the Hushed
        # These are listed here even though you can kill Horace in the Road of Sacrifices because
        # the player may want to complete his and Anri's quest first.
        DS3LocationData("SL: Llewellyn Shield",                    "Llewellyn Shield",                  DS3LocationCategory.SHIELD,
                        npc = True), # kill or quest
        # Shrine Handmaiden after killing
        DS3LocationData("SL: Executioner Helm",                    "Executioner Helm",                  DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),
        DS3LocationData("SL: Executioner Armor",                   "Executioner Armor",                 DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),
        DS3LocationData("SL: Executioner Gauntlets",               "Executioner Gauntlets",             DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),
        DS3LocationData("SL: Executioner Leggings",                "Executioner Leggings",              DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),

        # Shrine Handmaid after killing Knight Slayer Tsorig
        DS3LocationData("SL: Black Iron Helm",                     "Black Iron Helm",                   DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("SL: Black Iron Armor",                    "Black Iron Armor",                  DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("SL: Black Iron Gauntlets",                "Black Iron Gauntlets",              DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("SL: Black Iron Leggings",                 "Black Iron Leggings",               DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),

        # Near Cornyx's cage after killing Old Demon King with Cuculus
        DS3LocationData("SL: Spotted Whip",                        "Spotted Whip",                      DS3LocationCategory.WEAPON,
                        missable = True, boss = True, npc = True),
        DS3LocationData("SL: Cornyx's Garb",                       "Cornyx's Garb",                     DS3LocationCategory.ARMOR,
                        offline = '02,0:53100100::', missable = True, boss = True, npc = True),
        DS3LocationData("SL: Cornyx's Wrap",                       "Cornyx's Wrap",                     DS3LocationCategory.ARMOR,
                        offline = '02,0:53100100::', missable = True, boss = True, npc = True),
        DS3LocationData("SL: Cornyx's Skirt",                      "Cornyx's Skirt",                    DS3LocationCategory.ARMOR,
                        offline = '02,0:53100100::', missable = True, boss = True, npc = True),
    ],
    "Irithyll of the Boreal Valley": [
        DS3LocationData("IBV: Soul of Pontiff Sulyvahn",           "Soul of Pontiff Sulyvahn",          DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier #1", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Large Titanite Shard #1",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Soul of a Weary Warrior #1",         "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Soul of a Weary Warrior #2",         "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Rime-blue Moss Clump #1",            "Rime-blue Moss Clump",              DS3LocationCategory.MISC),
        DS3LocationData("IBV: Witchtree Branch",                   "Witchtree Branch",                  DS3LocationCategory.WEAPON,
                        hidden = True), # Behind illusory wall
        DS3LocationData("IBV: Large Titanite Shard #2",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Budding Green Blossom",              "Budding Green Blossom",             DS3LocationCategory.MISC),
        DS3LocationData("IBV: Rime-blue Moss Clump #2",            "Rime-blue Moss Clump x2",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Large Titanite Shard #3",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Large Titanite Shard #4",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE,
                        hidden = True), # Behind illusory wall
        DS3LocationData("IBV: Large Soul of a Nameless Soldier #2", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Large Titanite Shard #5",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Large Titanite Shard #6",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Soul of a Weary Warrior #3",         "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Magic Clutch Ring",                  "Magic Clutch Ring",                 DS3LocationCategory.RING,
                        hidden = True), # Behind illusory wall
        DS3LocationData("IBV: Fading Soul #1",                     "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("IBV: Fading Soul #2",                     "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("IBV: Homeward Bone",                      "Homeward Bone x3",                  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Undead Bone Shard",                  "Undead Bone Shard",                 DS3LocationCategory.HEALTH,
                        hidden = True), # Hidden behind gravestone
        DS3LocationData("IBV: Kukri",                              "Kukri x8",                          DS3LocationCategory.MISC),
        DS3LocationData("IBV: Rusted Gold Coin #1",                "Rusted Gold Coin",                  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Blue Bug Pellet #1",                 "Blue Bug Pellet x2",                DS3LocationCategory.MISC),
        DS3LocationData("IBV: Shriving Stone",                     "Shriving Stone",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Blood Gem",                          "Blood Gem",                         DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Green Blossom #1",                   "Green Blossom x3",                  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Ring of Sacrifice",                  "Ring of Sacrifice",                 DS3LocationCategory.MISC),
        DS3LocationData("IBV: Great Heal",                         "Great Heal",                        DS3LocationCategory.SPELL),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier #3", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Green Blossom #2",                   "Green Blossom x3",                  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Dung Pie #1",                        "Dung Pie x3",                       DS3LocationCategory.MISC),
        DS3LocationData("IBV: Dung Pie #2",                        "Dung Pie x3",                       DS3LocationCategory.MISC),
        # These don't actually guard any single item sales. Maybe we can inject one manually?
        DS3LocationData("IBV: Excrement-covered Ashes",            "Excrement-covered Ashes",           DS3LocationCategory.UNIQUE),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier #4", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Soul of a Weary Warrior #4",         "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Large Titanite Shard #7",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Blue Bug Pellet #2",                 "Blue Bug Pellet x2",                DS3LocationCategory.MISC),
        DS3LocationData("IBV: Ember",                              "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("IBV: Large Titanite Shard #8",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Green Blossom #3",                   "Green Blossom",                     DS3LocationCategory.MISC),
        DS3LocationData("IBV: Lightning Gem",                      "Lightning Gem",                     DS3LocationCategory.UPGRADE),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier #5", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("IBV: Soul of a Weary Warrior #5",         "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Proof of a Concord Kept",            "Proof of a Concord Kept",           DS3LocationCategory.MISC),
        DS3LocationData("IBV: Rusted Gold Coin #2",                "Rusted Gold Coin",                  DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("IBV: Chloranthy Ring+1",                  "Chloranthy Ring+1",                 DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("IBV: Covetous Gold Serpent Ring+1",       "Covetous Gold Serpent Ring+1",      DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Hidden fall
        DS3LocationData("IBV: Wood Grain Ring+2",                  "Wood Grain Ring+2",                 DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("IBV: Divine Blessing #1",                 "Divine Blessing",                   DS3LocationCategory.MISC),
        DS3LocationData("IBV: Smough's Great Hammer",              "Smough's Great Hammer",             DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Yorshka's Spear",                    "Yorshka's Spear",                   DS3LocationCategory.WEAPON),
        DS3LocationData("IBV: Leo Ring",                           "Leo Ring",                          DS3LocationCategory.RING),
        DS3LocationData("IBV: Dorhys' Gnawing",                    "Dorhys' Gnawing",                   DS3LocationCategory.SPELL,
                        hidden = True), # Behind illusory wall
        DS3LocationData("IBV: Divine Blessing #2",                 "Divine Blessing",                   DS3LocationCategory.MISC,
                        hidden = True), # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard #9",            "Large Titanite Shard",              DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard #10",           "Large Titanite Shard x2",           DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard #11",           "Large Titanite Shard x2",           DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Roster of Knights",                  "Roster of Knights",                 DS3LocationCategory.UNIQUE),
        DS3LocationData("IBV: Twinkling Titanite #1",              "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True, hidden = True), # Behind illusory wall
        DS3LocationData("IBV: Twinkling Titanite #2",              "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("IBV: Siegbräu",                           "Siegbräu",                          DS3LocationCategory.MISC,
                        missable = True, npc = True),
        DS3LocationData("IBV: Emit Force",                         "Emit Force",                        DS3LocationCategory.SPELL,
                        missable = True, npc = True),
        DS3LocationData("IBV: Sneering Mask",                      "Sneering Mask",                     DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True), # Londor Pale Shade (win both invasions)
        DS3LocationData("IBV: Pale Shade Robe",                    "Pale Shade Robe",                   DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True), # Londor Pale Shade (win both invasions)
        DS3LocationData("IBV: Pale Shade Gloves",                  "Pale Shade Gloves",                 DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True), # Londor Pale Shade (win both invasions)
        DS3LocationData("IBV: Pale Shade Trousers",                "Pale Shade Trousers",               DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True), # Londor Pale Shade (win both invasions)
        DS3LocationData("IBV: Greatsword of Judgment",             "Greatsword of Judgment",            DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("IBV: Profaned Greatsword",                "Profaned Greatsword",               DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Anri of Astora
        DS3LocationData("IBV: Anri's Straight Sword",              "Anri's Straight Sword",             DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("IBV: Ring of the Evil Eye",               "Ring of the Evil Eye",              DS3LocationCategory.RING,
                        missable = True, npc = True),

        # Shrine Handmaid after killing Sulyvahn's Beast Duo
        DS3LocationData("IBV: Helm of Favor",                      "Helm of Favor",                     DS3LocationCategory.ARMOR,
                        hidden = True, miniboss = True, shop = True),
        DS3LocationData("IBV: Embraced Armor of Favor",            "Embraced Armor of Favor",           DS3LocationCategory.ARMOR,
                        hidden = True, miniboss = True, shop = True),
        DS3LocationData("IBV: Gauntlets of Favor",                 "Gauntlets of Favor",                DS3LocationCategory.ARMOR,
                        hidden = True, miniboss = True, shop = True),
        DS3LocationData("IBV: Leggings of Favor",                  "Leggings of Favor",                 DS3LocationCategory.ARMOR,
                        hidden = True, miniboss = True, shop = True),

        # Sirris after killing Creighton
        DS3LocationData("IBV: Mail Breaker",                       "Mail Breaker",                      DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("IBC: Silvercat Ring",                     "Silvercat Ring",                    DS3LocationCategory.RING,
                        missable = True, npc = True),
        DS3LocationData("IBV: Dragonslayer's Axe",                 "Dragonslayer's Axe",                DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("IBV: Creighton's Steel Mask",             "Creighton's Steel Mask",            DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("IBV: Mirrah Chain Mail",                  "Mirrah Chain Mail",                 DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("IBV: Mirrah Chain Gloves",                "Mirrah Chain Gloves",               DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("IBV: Mirrah Chain Leggings",              "Mirrah Chain Leggings",             DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
    ],
    "Irithyll Dungeon": [
        DS3LocationData("ID: Titanite Slab",                       "Titanite Slab",                     DS3LocationCategory.UPGRADE,
                        missable = True, npc = True), # Siegward (quest)
        DS3LocationData("ID: Murakumo",                            "Murakumo",                          DS3LocationCategory.WEAPON,
                        missable = True, npc = True), # Alva (requires ember)
        DS3LocationData("ID: Large Titanite Shard #1",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Fading Soul",                         "Fading Soul",                       DS3LocationCategory.MISC),
        DS3LocationData("ID: Large Soul of a Nameless Soldier #1", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("ID: Jailbreaker's Key",                   "Jailbreaker's Key",                 DS3LocationCategory.KEY,
                        key = True),
        DS3LocationData("ID: Pale Pine Resin",                     "Pale Pine Resin x2",                DS3LocationCategory.MISC),
        DS3LocationData("ID: Simple Gem",                          "Simple Gem",                        DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Large Soul of a Nameless Soldier #2", "Large Soul of a Nameless Soldier",  DS3LocationCategory.MISC),
        DS3LocationData("ID: Large Titanite Shard #2",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Homeward Bone",                       "Homeward Bone x2",                  DS3LocationCategory.MISC),
        DS3LocationData("ID: Bellowing Dragoncrest Ring",          "Bellowing Dragoncrest Ring",        DS3LocationCategory.RING),
        DS3LocationData("ID: Soul of a Weary Warrior #1",          "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("ID: Soul of a Crestfallen Knight",        "Soul of a Crestfallen Knight",      DS3LocationCategory.MISC),
        DS3LocationData("ID: Lightning Bolt",                      "Lightning Bolt x9",                 DS3LocationCategory.MISC),
        DS3LocationData("ID: Large Titanite Shard #3",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Profaned Flame",                      "Profaned Flame",                    DS3LocationCategory.SPELL),
        DS3LocationData("ID: Large Titanite Shard #4",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Soul of a Weary Warrior #2",          "Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("ID: Dung Pie #1",                         "Dung Pie x4",                       DS3LocationCategory.MISC),
        DS3LocationData("ID: Ember #1",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("ID: Ember #2",                            "Ember",                             DS3LocationCategory.MISC),
        DS3LocationData("ID: Profaned Coal",                       "Profaned Coal",                     DS3LocationCategory.UNIQUE),
        DS3LocationData("ID: Large Titanite Shard #5",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Old Sorcerer Hat",                    "Old Sorcerer Hat",                  DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Coat",                   "Old Sorcerer Coat",                 DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Gauntlets",              "Old Sorcerer Gauntlets",            DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Old Sorcerer Boots",                  "Old Sorcerer Boots",                DS3LocationCategory.ARMOR),
        DS3LocationData("ID: Large Soul of a Weary Warrior",       "Large Soul of a Weary Warrior",     DS3LocationCategory.MISC),
        DS3LocationData("ID: Covetous Gold Serpent Ring",          "Covetous Gold Serpent Ring",        DS3LocationCategory.RING),
        DS3LocationData("ID: Lightning Blade",                     "Lightning Blade",                   DS3LocationCategory.SPELL),
        DS3LocationData("ID: Rusted Coin",                         "Rusted Coin",                       DS3LocationCategory.MISC),
        DS3LocationData("ID: Dusk Crown Ring",                     "Dusk Crown Ring",                   DS3LocationCategory.RING),
        DS3LocationData("ID: Pickaxe",                             "Pickaxe",                           DS3LocationCategory.WEAPON),
        DS3LocationData("ID: Xanthous Ashes",                      "Xanthous Ashes",                    DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("ID: Rusted Gold Coin",                    "Rusted Gold Coin",                  DS3LocationCategory.MISC),
        DS3LocationData("ID: Large Titanite Shard #6",             "Large Titanite Shard",              DS3LocationCategory.UPGRADE),
        DS3LocationData("ID: Old Cell Key",                        "Old Cell Key",                      DS3LocationCategory.KEY,
                        key = True),
        DS3LocationData("ID: Covetous Silver Serpent Ring+1",      "Covetous Silver Serpent Ring+1",    DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("ID: Dragon Torso Stone",                  "Dragon Torso Stone",                DS3LocationCategory.UNIQUE),
        DS3LocationData("ID: Prisoner Chief's Ashes",              "Prisoner Chief's Ashes",            DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("ID: Great Magic Shield",                  "Great Magic Shield",                DS3LocationCategory.SPELL,
                        hidden = True), # Guaranteed drop from a normal-looking Corpse-Grub
        DS3LocationData("ID: Dragonslayer Lightning Arrow",        "Dragonslayer Lightning Arrow x10",  DS3LocationCategory.MISC,
                        mimic = True),
        DS3LocationData("ID: Titanite Scale #1",                   "Titanite Scale x2",                 DS3LocationCategory.UPGRADE,
                        mimic = True),
        DS3LocationData("ID: Dark Clutch Ring",                    "Dark Clutch Ring",                  DS3LocationCategory.RING,
                        mimic = True),
        DS3LocationData("ID: Estus Shard",                         "Estus Shard",                       DS3LocationCategory.HEALTH,
                        mimic = True),
        DS3LocationData("ID: Titanite Chunk #1",                   "Titanite Chunk",                    DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("ID: Titanite Scale #2",                   "Titanite Scale",                    DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("ID: Dung Pie #2",                         "Dung Pie x4",                       DS3LocationCategory.MISC),
        DS3LocationData("ID: Titanite Chunk #2",                   "Titanite Chunk",                    DS3LocationCategory.UPGRADE,
                        miniboss = True), # Giant Slave Drop

        # Alva (requires ember)
        DS3LocationData("ID: Alva Helm",                           "Alva Helm",                         DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("ID: Alva Armor",                          "Alva Armor",                        DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("ID: Alva Gauntlets",                      "Alva Gauntlets",                    DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("ID: Alva Leggings",                       "Alva Leggings",                     DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
    ],
    "Profaned Capital": [
        DS3LocationData("PC: Soul of Yhorm the Giant",             "Soul of Yhorm the Giant",             DS3LocationCategory.BOSS,
                        boss = True),
        DS3LocationData("PC: Cinders of a Lord - Yhorm the Giant", "Cinders of a Lord - Yhorm the Giant", DS3LocationCategory.KEY,
                        offline = "07,0:50002170::", prominent = True, progression = True, boss = True),
        DS3LocationData("PC: Logan's Scroll",                      "Logan's Scroll",                      DS3LocationCategory.UNIQUE,
                        hostile_npc = True), # Sorcerer
        DS3LocationData("PC: Purging Stone #1",                    "Purging Stone x3",                    DS3LocationCategory.MISC),
        DS3LocationData("PC: Rusted Coin #1",                      "Rusted Coin x2",                      DS3LocationCategory.MISC),
        DS3LocationData("PC: Rusted Gold Coin #1",                 "Rusted Gold Coin",                    DS3LocationCategory.MISC),
        DS3LocationData("PC: Purging Stone #2",                    "Purging Stone",                       DS3LocationCategory.MISC),
        DS3LocationData("PC: Cursebite Ring",                      "Cursebite Ring",                      DS3LocationCategory.RING),
        DS3LocationData("PC: Poison Gem",                          "Poison Gem",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("PC: Shriving Stone",                      "Shriving Stone",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("PC: Poison Arrow",                        "Poison Arrow x18",                    DS3LocationCategory.MISC),
        DS3LocationData("PC: Rubbish",                             "Rubbish",                             DS3LocationCategory.MISC),
        DS3LocationData("PC: Onislayer Greatarrow",                "Onislayer Greatarrow x8",             DS3LocationCategory.MISC),
        DS3LocationData("PC: Large Soul of a Weary Warrior",       "Large Soul of a Weary Warrior",       DS3LocationCategory.MISC),
        DS3LocationData("PC: Rusted Coin #2",                      "Rusted Coin",                         DS3LocationCategory.MISC),
        DS3LocationData("PC: Rusted Coin #3",                      "Rusted Coin",                         DS3LocationCategory.MISC),
        DS3LocationData("PC: Blooming Purple Moss Clump",          "Blooming Purple Moss Clump x3",       DS3LocationCategory.MISC),
        DS3LocationData("PC: Wrath of the Gods",                   "Wrath of the Gods",                   DS3LocationCategory.SPELL),
        DS3LocationData("PC: Onislayer Greatbow",                  "Onislayer Greatbow",                  DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("PC: Jailer's Key Ring",                   "Jailer's Key Ring",                   DS3LocationCategory.KEY,
                        progression = True, key = True),
        DS3LocationData("PC: Ember",                               "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("PC: Flame Stoneplate Ring+1",             "Flame Stoneplate Ring+1",             DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("PC: Magic Stoneplate Ring+2",             "Magic Stoneplate Ring+2",             DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("PC: Court Sorcerer Hood",                 "Court Sorcerer Hood",                 DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Robe",                 "Court Sorcerer Robe",                 DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Gloves",               "Court Sorcerer Gloves",               DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Court Sorcerer Trousers",             "Court Sorcerer Trousers",             DS3LocationCategory.ARMOR),
        DS3LocationData("PC: Storm Ruler",                         "Storm Ruler",                         DS3LocationCategory.KEY),
        DS3LocationData("PC: Undead Bone Shard",                   "Undead Bone Shard",                   DS3LocationCategory.HEALTH),
        DS3LocationData("PC: Eleonora",                            "Eleonora",                            DS3LocationCategory.WEAPON,
                        hidden = True), # Guaranteed drop from a normal-looking Monstrosity of Sin
        DS3LocationData("PC: Rusted Gold Coin #2",                 "Rusted Gold Coin x2",                 DS3LocationCategory.MISC,
                        mimic = True),
        DS3LocationData("PC: Court Sorcerer's Staff",              "Court Sorcerer's Staff",              DS3LocationCategory.WEAPON,
                        mimic = True),
        DS3LocationData("PC: Greatshield of Glory",                "Greatshield of Glory",                DS3LocationCategory.SHIELD,
                        mimic = True),
        DS3LocationData("PC: Twinkling Titanite #1",               "Twinkling Titanite",                  DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PC: Twinkling Titanite #2",               "Twinkling Titanite",                  DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("US: Siegbräu",                            "Siegbräu",                            DS3LocationCategory.MISC,
                        missable = True, npc = True),
        DS3LocationData("PC: Yhorm's Great Machete",               "Yhorm's Great Machete",               DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("PC: Yhorm's Greatshield",                 "Yhorm's Greatshield",                 DS3LocationCategory.SHIELD,
                        missable = True, boss = True, shop = True),

        # Siegward drops (kill or quest)
        DS3LocationData("PC: Storm Ruler (Siegward)",              "Storm Ruler",                         DS3LocationCategory.WEAPON,
                        offline = '02,0:50006218::', missable = True, npc = True),
        DS3LocationData("PC: Pierce Shield",                       "Pierce Shield",                       DS3LocationCategory.SHIELD,
                        missable = True, npc = True),
    ],
    # We consider "Anor Londo" to be everything accessible only after killing Pontiff. This doesn't
    # match up one-to-one with where the game pops up the region name, but it balances items better
    # and covers the region that's full of DS1 Anor Londo references.
    "Anor Londo": [
        DS3LocationData("AL: Soul of Aldrich",                     "Soul of Aldrich",                     DS3LocationCategory.BOSS,
                        boss = True),
        DS3LocationData("AL: Cinders of a Lord - Aldrich",         "Cinders of a Lord - Aldrich",         DS3LocationCategory.KEY,
                        offline = '06,0:50002130::', prominent = True, progression = True, boss = True),
        DS3LocationData("AL: Yorshka's Chime",                     "Yorshka's Chime",                     DS3LocationCategory.WEAPON,
                        missable = True, npc = True), # Yorshka (kill), invisible walkway
        DS3LocationData("AL: Drang Twinspears",                    "Drang Twinspears",                    DS3LocationCategory.WEAPON,
                        hidden = True), # Guaranteed drop from a normal-loking knight
        DS3LocationData("AL: Estus Shard",                         "Estus Shard",                         DS3LocationCategory.HEALTH),
        DS3LocationData("AL: Painting Guardian's Curved Sword",    "Painting Guardian's Curved Sword",    DS3LocationCategory.WEAPON,
                        hidden = True), # Invisible walkway
        DS3LocationData("AL: Brass Helm",                          "Brass Helm",                          DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Brass Armor",                         "Brass Armor",                         DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Brass Gauntlets",                     "Brass Gauntlets",                     DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Brass Leggings",                      "Brass Leggings",                      DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Human Dregs",                         "Human Dregs",                         DS3LocationCategory.MISC,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Ember #1",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("AL: Large Titanite Shard #1",             "Large Titanite Shard",                DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Large Titanite Shard #2",             "Large Titanite Shard",                DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Soul of a Weary Warrior",             "Soul of a Weary Warrior",             DS3LocationCategory.MISC),
        DS3LocationData("AL: Ember #2",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("AL: Ember #3",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("AL: Large Titanite Shard #3",             "Large Titanite Shard",                DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Dark Stoneplate Ring",                "Dark Stoneplate Ring",                DS3LocationCategory.RING),
        DS3LocationData("AL: Large Titanite Shard #4",             "Large Titanite Shard",                DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Deep Gem",                            "Deep Gem",                            DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Titanite Scale",                      "Titanite Scale",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("AL: Dragonslayer Greatarrow",             "Dragonslayer Greatarrow x5",          DS3LocationCategory.MISC,
                        offline = '06,0:53700620::', hidden = True), # Hidden fall
        DS3LocationData("AL: Dragonslayer Greatbow",               "Dragonslayer Greatbow",               DS3LocationCategory.WEAPON,
                        offline = '06,0:53700620::', hidden = True), # Hidden fall
        DS3LocationData("AL: Easterner's Ashes",                   "Easterner's Ashes",                   DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("AL: Painting Guardian Hood",              "Painting Guardian Hood",              DS3LocationCategory.ARMOR,
                        hidden = True), # Invisible walkway
        DS3LocationData("AL: Painting Guardian Gown",              "Painting Guardian Gown",              DS3LocationCategory.ARMOR,
                        hidden = True), # Invisible walkway
        DS3LocationData("AL: Painting Guardian Gloves",            "Painting Guardian Gloves",            DS3LocationCategory.ARMOR,
                        hidden = True), # Invisible walkway
        DS3LocationData("AL: Painting Guardian Waistcloth",        "Painting Guardian Waistcloth",        DS3LocationCategory.ARMOR,
                        hidden = True), # Invisible walkway
        DS3LocationData("AL: Soul of a Crestfallen Knight",        "Soul of a Crestfallen Knight",        DS3LocationCategory.MISC),
        DS3LocationData("AL: Moonlight Arrow",                     "Moonlight Arrow x6",                  DS3LocationCategory.MISC),
        DS3LocationData("AL: Proof of a Concord Kept",             "Proof of a Concord Kept",             DS3LocationCategory.MISC),
        DS3LocationData("AL: Large Soul of a Weary Warrior",       "Large Soul of a Weary Warrior",       DS3LocationCategory.MISC),
        DS3LocationData("AL: Giant's Coal",                        "Giant's Coal",                        DS3LocationCategory.UNIQUE),
        DS3LocationData("AL: Havel's Ring+2",                      "Havel's Ring+2",                      DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Invisible walkway
        DS3LocationData("AL: Ring of Favor+1",                     "Ring of Favor+1",                     DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("AL: Sun Princess Ring",                   "Sun Princess Ring",                   DS3LocationCategory.RING),
        DS3LocationData("AL: Reversal Ring",                       "Reversal Ring",                       DS3LocationCategory.RING,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Golden Ritual Spear",                 "Golden Ritual Spear",                 DS3LocationCategory.WEAPON,
                        mimic = True),
        DS3LocationData("AL: Ring of Favor",                       "Ring of Favor",                       DS3LocationCategory.RING,
                        miniboss = True, hidden = True), # Sulyvahn's Beast Duo drop, behind illusory wall
        DS3LocationData("AL: Blade of the Darkmoon",               "Blade of the Darkmoon",               DS3LocationCategory.UNIQUE,
                        missable = True, npc = True), # Yorshka (quest or kill)
        DS3LocationData("AL: Simple Gem",                          "Simple Gem",                          DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("AL: Twinkling Titanite #1",               "Twinkling Titanite",                  DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("AL: Twinkling Titanite #2",               "Twinkling Titanite",                  DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("AL: Aldrich's Ruby",                      "Aldrich's Ruby",                      DS3LocationCategory.RING,
                        miniboss = True), # Deep Accursed drop
        DS3LocationData("AL: Aldrich Faithful",                    "Aldrich Faithful",                    DS3LocationCategory.UNIQUE,
                        hidden = True), # Behind illusory wall
        DS3LocationData("AL: Budding Green Blossom",               "Budding Green Blossom",               DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,70000118:', missable = True, npc = True, shop = True), # sold by Shrine Maiden after helping Sirris and defeating Aldrich
        DS3LocationData("AL: Bountiful Sunlight",                  "Bountiful Sunlight",                  DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
        DS3LocationData("AL: Darkmoon Longbow",                    "Darkmoon Longbow",                    DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("AL: Lifehunt Scythe",                     "Lifehunt Scythe",                     DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Sirris (quest completion)
        DS3LocationData("AL: Sunset Shield",                       "Sunset Shield",                       DS3LocationCategory.SHIELD,
                        missable = True, npc = True),
        DS3LocationData("AL: Sunless Talisman",                    "Sunless Talisman",                    DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("AL: Sunless Veil",                        "Sunless Veil",                        DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Sunless Armor",                       "Sunless Armor",                       DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Sunless Gauntlets",                   "Sunless Gauntlets",                   DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Sunless Leggings",                    "Sunless Leggings",                    DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        # In Pit of Hollows after completion
        DS3LocationData("AL: Sunset Helm",                         "Sunset Helm",                         DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("AL: Sunset Armor",                        "Sunset Armor",                        DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("AL: Sunset Gauntlets",                    "Sunset Gauntlets",                    DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("AL: Sunset Leggings",                     "Sunset Leggings",                     DS3LocationCategory.ARMOR,
                        missable = True, npc = True),

        # Anri of Astora
        DS3LocationData("AL: Chameleon",                          "Chameleon",                            DS3LocationCategory.SPELL,
                        missable = True, npc = True),

        # Shrine Handmaid after killing Ringfinger Leonhard
        # This is listed here even though you can kill Leonhard immediately because we don't want to
        # make people do that until they have a chance to complete his quest and Sirris's.
        DS3LocationData("AL: Leonhard's Garb",                     "Leonhard's Garb",                     DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),
        DS3LocationData("AL: Leonhard's Gauntlets",                "Leonhard's Gauntlets",                DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),
        DS3LocationData("AL: Leonhard's Trousers",                 "Leonhard's Trousers",                 DS3LocationCategory.ARMOR,
                        hidden = True, npc = True, shop = True),

        # Shrine Handmaid after killing Alrich, Devourer of Gods
        DS3LocationData("AL: Smough's Helm",                       "Smough's Helm",                       DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AL: Smough's Armor",                      "Smough's Armor",                      DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AL: Smough's Gauntlets",                  "Smough's Gauntlets",                  DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AL: Smough's Leggings",                   "Smough's Leggings",                   DS3LocationCategory.ARMOR,
                        boss = True, shop = True),

        # Shrine Handmaid after killing Anri or completing their quest
        DS3LocationData("AL: Elite Knight Helm",                   "Elite Knight Helm",                   DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Elite Knight Armor",                  "Elite Knight Armor",                  DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Elite Knight Gauntlets",              "Elite Knight Gauntlets",              DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("AL: Elite Knight Leggings",               "Elite Knight Leggings",               DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),

        # Ringfinger Leonhard (quest or kill)
        DS3LocationData("AL: Crescent Moon Sword",                 "Crescent Moon Sword",                 DS3LocationCategory.WEAPON,
                        missable = True, npc = True),
        DS3LocationData("AL: Silver Mask",                         "Silver Mask",                         DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("AL: Soul of Rosaria",                     "Soul of Rosaria",                     DS3LocationCategory.UNIQUE,
                        missable = True, npc = True),

    ],
    "Lothric Castle": [
        DS3LocationData("LC: Soul of Dragonslayer Armour",         "Soul of Dragonslayer Armour",         DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("LC: Sniper Bolt",                         "Sniper Bolt x11",                     DS3LocationCategory.MISC),
        DS3LocationData("LC: Sniper Crossbow",                     "Sniper Crossbow",                     DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Titanite Scale #1",                   "Titanite Scale",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Chunk #1",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Greatlance",                          "Greatlance",                          DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Titanite Chunk #2",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Chunk #3",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Sacred Bloom Shield",                 "Sacred Bloom Shield",                 DS3LocationCategory.SHIELD,
                        hidden = True), # Behind illusory wall
        DS3LocationData("LC: Titanite Chunk #4",                   "Titanite Chunk x2",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Refined Gem",                         "Refined Gem",                         DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Soul of a Crestfallen Knight #1",     "Soul of a Crestfallen Knight",        DS3LocationCategory.MISC),
        DS3LocationData("LC: Undead Bone Shard",                   "Undead Bone Shard",                   DS3LocationCategory.HEALTH),
        DS3LocationData("LC: Lightning Urn #1",                    "Lightning Urn x3",                    DS3LocationCategory.MISC),
        DS3LocationData("LC: Titanite Chunk #5",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Chunk #6",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Chunk #7",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Caitha's Chime",                      "Caitha's Chime",                      DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Lightning Urn #2",                    "Lightning Urn x6",                    DS3LocationCategory.MISC),
        DS3LocationData("LC: Ember #1",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("LC: Raw Gem",                             "Raw Gem",                             DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Black Firebomb",                      "Black Firebomb x3",                   DS3LocationCategory.MISC),
        DS3LocationData("LC: Pale Pine Resin",                     "Pale Pine Resin",                     DS3LocationCategory.MISC),
        DS3LocationData("LC: Large Soul of a Weary Warrior #1",    "Large Soul of a Weary Warrior",       DS3LocationCategory.MISC),
        DS3LocationData("LC: Sunlight Medal",                      "Sunlight Medal",                      DS3LocationCategory.MISC),
        DS3LocationData("LC: Soul of a Crestfallen Knight #2",     "Soul of a Crestfallen Knight",        DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("LC: Titanite Chunk #8",                   "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Scale #2",                   "Titanite Scale",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Large Soul of a Nameless Soldier #1", "Large Soul of a Nameless Soldier",    DS3LocationCategory.MISC),
        DS3LocationData("LC: Knight's Ring",                       "Knight's Ring",                       DS3LocationCategory.RING),
        DS3LocationData("LC: Ember #2",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("LC: Large Soul of a Weary Warrior #2",    "Large Soul of a Weary Warrior",       DS3LocationCategory.MISC),
        DS3LocationData("LC: Ember #3",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("LC: Twinkling Titanite #1",               "Twinkling Titanite",                  DS3LocationCategory.MISC),
        DS3LocationData("LC: Large Soul of a Nameless Soldier #2", "Large Soul of a Nameless Soldier",    DS3LocationCategory.MISC),
        DS3LocationData("LC: Ember #4",                            "Ember",                               DS3LocationCategory.MISC),
        DS3LocationData("LC: Winged Knight Helm",                  "Winged Knight Helm",                  DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("LC: Winged Knight Armor",                 "Winged Knight Armor",                 DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("LC: Winged Knight Gauntlets",             "Winged Knight Gauntlets",             DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("LC: Winged Knight Leggings",              "Winged Knight Leggings",              DS3LocationCategory.ARMOR,
                        hidden = True), # Behind illusory wall
        DS3LocationData("LC: Rusted Coin",                         "Rusted Coin x2",                      DS3LocationCategory.MISC),
        DS3LocationData("LC: Braille Divine Tome of Lothric",      "Braille Divine Tome of Lothric",      DS3LocationCategory.UNIQUE,
                        hidden = True), # Hidden fall
        DS3LocationData("LC: Red Tearstone Ring",                  "Red Tearstone Ring",                  DS3LocationCategory.RING),
        DS3LocationData("LC: Twinkling Titanite #2",               "Twinkling Titanite x2",               DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Large Soul of a Nameless Soldier #3", "Large Soul of a Nameless Soldier",    DS3LocationCategory.MISC),
        DS3LocationData("LC: Titanite Scale #3",                   "Titanite Scale x3",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Titanite Scale #4",                   "Titanite Scale",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Hood of Prayer",                      "Hood of Prayer",                      DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Robe of Prayer",                      "Robe of Prayer",                      DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Skirt of Prayer",                     "Skirt of Prayer",                     DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Spirit Tree Crest Shield",            "Spirit Tree Crest Shield",            DS3LocationCategory.SHIELD),
        DS3LocationData("LC: Titanite Scale #5",                   "Titanite Scale",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Twinkling Titanite #3",               "Twinkling Titanite",                  DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Twinkling Titanite #4",               "Twinkling Titanite x2",               DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Life Ring+2",                         "Life Ring+2",                         DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Hidden fall
        DS3LocationData("LC: Dark Stoneplate Ring+1",              "Dark Stoneplate Ring+1",              DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Hidden fall
        DS3LocationData("LC: Thunder Stoneplate Ring+2",           "Thunder Stoneplate Ring+2",           DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("LC: Sunlight Straight Sword",             "Sunlight Straight Sword",             DS3LocationCategory.WEAPON,
                        mimic = True, hidden = True), # Hidden fall
        DS3LocationData("LC: Titanite Scale #6",                   "Titanite Scale x3",                   DS3LocationCategory.UPGRADE,
                        mimic = True),
        DS3LocationData("LC: Ember #5",                            "Ember x2",                            DS3LocationCategory.MISC,
                        miniboss = True, hidden = True), # Hidden fall, Pus of Man Wyvern drop
        DS3LocationData("LC: Titanite Chunk #9",                   "Titanite Chunk x2",                   DS3LocationCategory.UPGRADE,
                        miniboss = True, hidden = True), # Hidden fall, Pus of Man Wyvern drop
        DS3LocationData("LC: Ember #6",                            "Ember x2",                            DS3LocationCategory.MISC,
                        miniboss = True), # Pus of Man Wyvern drop
        DS3LocationData("LC: Titanite Chunk #10",                  "Titanite Chunk x2",                   DS3LocationCategory.UPGRADE,
                        miniboss = True),
        DS3LocationData("LC: Irithyll Rapier",                     "Irithyll Rapier",                     DS3LocationCategory.WEAPON,
                        miniboss = True), # Boreal Outrider drop
        DS3LocationData("LC: Twinkling Titanite #5",               "Twinkling Titanite x2",               DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("LC: Twinkling Titanite #6",               "Twinkling Titanite x2",               DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("LC: Gotthard Twinswords",                 "Gotthard Twinswords",                 DS3LocationCategory.WEAPON),
        DS3LocationData("LC: Grand Archives Key",                  "Grand Archives Key",                  DS3LocationCategory.KEY,
                        prominent = True, progression = True, key = True),
        DS3LocationData("LC: Titanite Chunk #11",                  "Titanite Chunk",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("LC: Dancer's Enchanted Swords",           "Dancer's Enchanted Swords",           DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("LC: Soothing Sunlight",                   "Soothing Sunlight",                   DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
        DS3LocationData("LC: Dragonslayer Greataxe",               "Dragonslayer Greataxe",               DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("LC: Dragonslayer Greatshield",            "Dragonslayer Greatshield",            DS3LocationCategory.SHIELD,
                        missable = True, boss = True, shop = True),

        # Eygon of Carim (kill or quest)
        DS3LocationData("LC: Morne's Great Hammer",                "Morne's Great Hammer",                DS3LocationCategory.WEAPON,
                        npc = True),
        DS3LocationData("LC: Moaning Shield",                      "Moaning Shield",                      DS3LocationCategory.SHIELD,
                        npc = True),

        # Shrine Handmaid after killing Dancer of the Boreal Valley
        DS3LocationData("LC: Dancer's Crown",                      "Dancer's Crown",                      DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("LC: Dancer's Armor",                      "Dancer's Armor",                      DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("LC: Dancer's Gauntlets",                  "Dancer's Gauntlets",                  DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("LC: Dancer's Leggings",                   "Dancer's Leggings",                   DS3LocationCategory.ARMOR,
                        boss = True, shop = True),

        # Shrine Handmaid after killing Dragonslayer Armour (or Eygon of Carim)
        DS3LocationData("LC: Morne's Helm",                        "Morne's Helm",                        DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Morne's Armor",                       "Morne's Armor",                       DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Morne's Gauntlets",                   "Morne's Gauntlets",                   DS3LocationCategory.ARMOR),
        DS3LocationData("LC: Morne's Leggings",                    "Morne's Leggings",                    DS3LocationCategory.ARMOR),
    ],
    "Consumed King's Garden": [

        DS3LocationData("CKG: Soul of Consumed Oceiros",           "Soul of Consumed Oceiros",                DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        # Could classify this as "hidden" because it's midway down an elevator, but the elevator is
        # so slow and the midway point is so obvious that it's not actually hard to find.
        DS3LocationData("CKG: Estus Shard",                        "Estus Shard",                             DS3LocationCategory.HEALTH),
        DS3LocationData("CKG: Shadow Mask",                        "Shadow Mask",                             DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Garb",                        "Shadow Garb",                             DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Gauntlets",                   "Shadow Gauntlets",                        DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Shadow Leggings",                    "Shadow Leggings",                         DS3LocationCategory.ARMOR),
        DS3LocationData("CKG: Black Firebomb",                     "Black Firebomb x2",                       DS3LocationCategory.MISC),
        DS3LocationData("CKG: Claw",                               "Claw",                                    DS3LocationCategory.WEAPON),
        DS3LocationData("CKG: Titanite Chunk #1",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Dragonscale Ring",                   "Dragonscale Ring",                        DS3LocationCategory.RING),
        DS3LocationData("CKG: Human Pine Resin #1",                "Human Pine Resin",                        DS3LocationCategory.MISC),
        DS3LocationData("CKG: Titanite Chunk #2",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Titanite Chunk #3",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Soul of a Weary Warrior",            "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("CKG: Dark Gem",                           "Dark Gem",                                DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Titanite Scale #1",                  "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Human Pine Resin #2",                "Human Pine Resin x2",                     DS3LocationCategory.MISC),
        DS3LocationData("CKG: Titanite Chunk #4",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Ring of Sacrifice",                  "Ring of Sacrifice",                       DS3LocationCategory.MISC),
        DS3LocationData("CKG: Wood Grain Ring+1",                  "Wood Grain Ring+1",                       DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CKG: Sage Ring+2",                        "Sage Ring+2",                             DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("CKG: Titanite Scale #2",                  "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Titanite Scale #3",                  "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("CKG: Magic Stoneplate Ring",              "Magic Stoneplate Ring",                   DS3LocationCategory.RING,
                        hidden = True), # Guaranteed drop from a normal-looking Consumed King's Knight
        DS3LocationData("CKG: Moonlight Greatsword",               "Moonlight Greatsword",                    DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("CKG: White Dragon Breath",                "White Dragon Breath",                     DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
    ],
    "Grand Archives": [
        # At the bottom of the shortcut elevator right outside the Twin Princes fight. Requires sending the elevator up to the top from the middle, and then riding the lower elevator down.
        DS3LocationData("GA: Titanite Slab #1",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        hidden = True), # Elevator secret
        DS3LocationData("GA: Soul of the Twin Princes",            "Soul of the Twin Princes",                DS3LocationCategory.BOSS,
                        boss = True),
        DS3LocationData("GA: Cinders of a Lord - Lothric Prince",  "Cinders of a Lord - Lothric Prince",      DS3LocationCategory.KEY,
                        offline = "09,0:50002040::", prominent = True, progression = True, boss = True),
        DS3LocationData("GA: Onikiri and Ubadachi",                "Onikiri and Ubadachi",                    DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Black Hand Kamui drop
        DS3LocationData("GA: Golden Wing Crest Shield",            "Golden Wing Crest Shield",                DS3LocationCategory.SHIELD,
                        hostile_npc = True), # Lion Knight Albert drop
        DS3LocationData("GA: Sage's Crystal Staff",                "Sage's Crystal Staff",                    DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Daughter of Crystal Kriemhild drop
        DS3LocationData("GA: Titanite Chunk #1",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Titanite Chunk #2",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Soul of a Crestfallen Knight #1",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("GA: Titanite Chunk #3",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Fleshbite Ring",                      "Fleshbite Ring",                          DS3LocationCategory.RING),
        DS3LocationData("GA: Soul of a Crestfallen Knight #2",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("GA: Soul of a Nameless Soldier",          "Soul of a Nameless Soldier",              DS3LocationCategory.MISC),
        DS3LocationData("GA: Crystal Chime",                       "Crystal Chime",                           DS3LocationCategory.WEAPON),
        DS3LocationData("GA: Titanite Scale #1",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Estus Shard",                         "Estus Shard",                             DS3LocationCategory.HEALTH),
        DS3LocationData("GA: Homeward Bone",                       "Homeward Bone x3",                        DS3LocationCategory.MISC),
        DS3LocationData("GA: Titanite Scale #2",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Titanite Chunk #4",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Hollow Gem",                          "Hollow Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Titanite Scale #3",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Titanite Scale #4",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Titanite Scale #5",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden by a table
        DS3LocationData("GA: Shriving Stone",                      "Shriving Stone",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Large Soul of a Crestfallen Knight #1", "Large Soul of a Crestfallen Knight",    DS3LocationCategory.MISC),
        DS3LocationData("GA: Titanite Chunk #5",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Titanite Scale #6",                   "Titanite Scale x3",                       DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Titanite Chunk #6",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Soul of a Weary Warrior",             "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("GA: Titanite Chunk #7",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Ember",                               "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("GA: Blessed Gem",                         "Blessed Gem",                             DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Titanite Chunk #8",                   "Titanite Chunk x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Large Soul of a Crestfallen Knight #2", "Large Soul of a Crestfallen Knight",    DS3LocationCategory.MISC),
        DS3LocationData("GA: Avelyn",                              "Avelyn",                                  DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Titanite Chunk #9",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Hunter's Ring",                       "Hunter's Ring",                           DS3LocationCategory.RING,
                        hostile_npc = True), # Daughter of Crystal Kriemhild drop
        DS3LocationData("GA: Divine Pillars of Light",             "Divine Pillars of Light",                 DS3LocationCategory.SPELL,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Power Within",                        "Power Within",                            DS3LocationCategory.SPELL,
                        hidden = True), # Switch in darkened room
        DS3LocationData("GA: Sage Ring+1",                         "Sage Ring+1",                             DS3LocationCategory.RING,
                        ngp = True, hidden = True), # Hidden fall
        DS3LocationData("GA: Lingering Dragoncrest Ring+2",        "Lingering Dragoncrest Ring+2",            DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("GA: Divine Blessing",                     "Divine Blessing",                         DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Twinkling Titanite #1",               "Twinkling Titanite x3",                   DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("GA: Witch's Locks",                       "Witch's Locks",                           DS3LocationCategory.WEAPON,
                        hidden = True), # Switch in darkened room
        DS3LocationData("GA: Titanite Slab #2",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        hidden = True), # Backtrack after flipping bridge switch
        DS3LocationData("GA: Titanite Scale #7",                   "Titanite Scale x3",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("GA: Soul Stream",                         "Soul Stream",                             DS3LocationCategory.SPELL,
                        hidden = True), # Behind illusory wall
        DS3LocationData("GA: Scholar Ring",                        "Scholar Ring",                            DS3LocationCategory.RING),
        DS3LocationData("GA: Undead Bone Shard",                   "Undead Bone Shard",                       DS3LocationCategory.HEALTH),
        DS3LocationData("GA: Titanite Slab #3",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from killing all Winged Knights
        DS3LocationData("GA: Outrider Knight Helm",                "Outrider Knight Helm",                    DS3LocationCategory.ARMOR,
                        miniboss = True, hidden = True), # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Armor",               "Outrider Knight Armor",                   DS3LocationCategory.ARMOR,
                        miniboss = True, hidden = True), # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Gauntlets",           "Outrider Knight Gauntlets",               DS3LocationCategory.ARMOR,
                        miniboss = True, hidden = True), # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Leggings",            "Outrider Knight Leggings",                DS3LocationCategory.ARMOR,
                        miniboss = True, hidden = True), # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Crystal Scroll",                      "Crystal Scroll",                          DS3LocationCategory.UNIQUE,
                        miniboss = True), # Crystal Sage drop
        DS3LocationData("GA: Twinkling Titanite #2",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Chaos Gem",                           "Chaos Gem",                               DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Twinkling Titanite #3",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Crystal Gem",                         "Crystal Gem",                             DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Twinkling Titanite #4",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Titanite Scale #8",                   "Titanite Scale x2",                       DS3LocationCategory.UPGRADE,
                        hidden = True, lizard = True), # Hidden fall
        DS3LocationData("GA: Twinkling Titanite #5",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Heavy Gem",                           "Heavy Gem",                               DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Twinkling Titanite #6",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Sharp Gem",                           "Sharp Gem",                               DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Twinkling Titanite #7",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Refined Gem",                         "Refined Gem",                             DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Twinkling Titanite #8",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("GA: Lorian's Greatsword",                 "Lorian's Greatsword",                     DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("GA: Lothric's Holy Sword",                "Lothric's Holy Sword",                    DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after killing NPCs
        DS3LocationData("GA: Faraam Helm",                         "Faraam Helm",                             DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("GA: Faraam Armor",                        "Faraam Armor",                            DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("GA: Faraam Gauntlets",                    "Faraam Gauntlets",                        DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("GA: Faraam Boots",                        "Faraam Boots",                            DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("GA: Black Hand Hat",                      "Black Hand Hat",                          DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),
        DS3LocationData("GA: Black Hand Armor",                    "Black Hand Armor",                        DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True, shop = True),

        # Shrine Handmaid after killing Lothric, Younger Prince
        DS3LocationData("GA: Lorian's Helm",                       "Lorian's Helm",                           DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("GA: Lorian's Armor",                      "Lorian's Armor",                          DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("GA: Lorian's Gauntlets",                  "Lorian's Gauntlets",                      DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("GA: Lorian's Leggings",                   "Lorian's Leggings",                       DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
    ],
    # The whole area is behind an illusory wall and thus marked hidden
    "Untended Graves": [
        DS3LocationData("UG: Soul of Champion Gundyr",             "Soul of Champion Gundyr",                 DS3LocationCategory.BOSS,
                        prominent = True, boss = True, hidden = True),
        DS3LocationData("UG: Priestess Ring",                      "Priestess Ring",                          DS3LocationCategory.RING,
                        hidden = True),
        DS3LocationData("UG: Shriving Stone",                      "Shriving Stone",                          DS3LocationCategory.UPGRADE,
                        hidden = True),
        DS3LocationData("UG: Titanite Chunk #1",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE,
                        hidden = True),
        DS3LocationData("UG: Soul of a Crestfallen Knight #1",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC,
                        hidden = True),
        DS3LocationData("UG: Titanite Chunk #2",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE,
                        hidden = True),
        DS3LocationData("UG: Ashen Estus Ring",                    "Ashen Estus Ring",                        DS3LocationCategory.RING,
                        hidden = True),
        DS3LocationData("UG: Black Knight Glaive",                 "Black Knight Glaive",                     DS3LocationCategory.WEAPON,
                        hidden = True),
        DS3LocationData("UG: Hidden Blessing",                     "Hidden Blessing",                         DS3LocationCategory.MISC,
                        hidden = True),
        DS3LocationData("UG: Eyes of a Fire Keeper",               "Eyes of a Fire Keeper",                   DS3LocationCategory.KEY,
                        hidden = True),
        DS3LocationData("UG: Soul of a Crestfallen Knight #2",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC,
                        hidden = True),
        DS3LocationData("UG: Blacksmith Hammer",                   "Blacksmith Hammer",                       DS3LocationCategory.WEAPON,
                        hidden = True),
        DS3LocationData("UG: Chaos Blade",                         "Chaos Blade",                             DS3LocationCategory.WEAPON,
                        hidden = True),
        DS3LocationData("UG: Coiled Sword Fragment",               "Coiled Sword Fragment",                   DS3LocationCategory.UNIQUE,
                        boss = True, hidden = True),
        DS3LocationData("UG: Life Ring+3",                         "Life Ring+3",                             DS3LocationCategory.RING,
                        ngp = True, hidden = True),
        DS3LocationData("UG: Ring of Steel Protection+1",          "Ring of Steel Protection+1",              DS3LocationCategory.RING,
                        ngp = True, hidden = True),
        DS3LocationData("UG: Hornet Ring",                         "Hornet Ring",                             DS3LocationCategory.RING,
                        hidden = True),
        DS3LocationData("FS: Gundyr's Halberd",                    "Gundyr's Halberd",                        DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("FS: Prisoner's Chain",                    "Prisoner's Chain",                        DS3LocationCategory.RING,
                        missable = True, boss = True, shop = True),

        # Yuria shop, or Shrine Handmaiden with Hollow's Ashes
        # This is here because this is where the ashes end up if you kill Yoel or Yuria
        DS3LocationData("UG: Ring of Sacrifice",                   "Ring of Sacrifice",                       DS3LocationCategory.MISC,
                        offline = '99,0:-1:40000,110000,70000107,70000116:', hidden = True, npc = True, shop = True),

        # Untended Graves Handmaid
        DS3LocationData("UG: Ember",                               "Ember",                                   DS3LocationCategory.RING,
                        hidden = True, shop = True),
        # Untended Graves Handmaid after killing Abyss Watchers
        DS3LocationData("UG: Wolf Knight Helm",                    "Wolf Knight Helm",                        DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("UG: Wolf Knight Armor",                   "Wolf Knight Armor",                       DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("UG: Wolf Knight Gauntlets",               "Wolf Knight Gauntlets",                   DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("UG: Wolf Knight Leggings",                "Wolf Knight Leggings",                    DS3LocationCategory.ARMOR,
                        boss = True, shop = True),

        # Shrine Handmaid after killing Champion Gundyr
        DS3LocationData("UG: Gundyr's Helm",                       "Gundyr's Helm",                           DS3LocationCategory.ARMOR,
                        hidden = True, boss = True, shop = True),
        DS3LocationData("UG: Gundyr's Armor",                      "Gundyr's Armor",                          DS3LocationCategory.ARMOR,
                        hidden = True, boss = True, shop = True),
        DS3LocationData("UG: Gundyr's Gauntlets",                  "Gundyr's Gauntlets",                      DS3LocationCategory.ARMOR,
                        hidden = True, boss = True, shop = True),
        DS3LocationData("UG: Gundyr's Leggings",                   "Gundyr's Leggings",                       DS3LocationCategory.ARMOR,
                        hidden = True, boss = True, shop = True),
    ],
    "Archdragon Peak": [
        DS3LocationData("AP: Dragon Head Stone",                   "Dragon Head Stone",                       DS3LocationCategory.UNIQUE,
                        prominent = True, boss = True),
        DS3LocationData("AP: Soul of the Nameless King",           "Soul of the Nameless King",               DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("AP: Dragon Tooth",                        "Dragon Tooth",                            DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Havel Knight drop
        DS3LocationData("AP: Havel's Greatshield",                 "Havel's Greatshield",                     DS3LocationCategory.SHIELD,
                        hostile_npc = True), # Havel Knight drop
        DS3LocationData("AP: Drakeblood Greatsword",               "Drakeblood Greatsword",                   DS3LocationCategory.WEAPON,
                        hostile_npc = True, hidden = True), # Drop from a summon who may or may not appear
        DS3LocationData("AP: Ricard's Rapier",                     "Ricard's Rapier",                         DS3LocationCategory.WEAPON,
                        hostile_npc = True, hidden = True), # Drop from a summon who may or may not appear
        DS3LocationData("AP: Lightning Clutch Ring",               "Lightning Clutch Ring",                   DS3LocationCategory.RING),
        DS3LocationData("AP: Stalk Dung Pie",                      "Stalk Dung Pie x6",                       DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Chunk #1",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Titanite Scale #1",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Soul of a Weary Warrior #1",          "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Chunk #2",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Lightning Gem",                       "Lightning Gem",                           DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Homeward Bone",                       "Homeward Bone x2",                        DS3LocationCategory.MISC),
        DS3LocationData("AP: Soul of a Nameless Soldier",          "Soul of a Nameless Soldier",              DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Chunk #3",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Ember #1",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("AP: Large Soul of a Weary Warrior",       "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("AP: Large Soul of a Nameless Soldier",    "Large Soul of a Nameless Soldier",        DS3LocationCategory.MISC),
        DS3LocationData("AP: Lightning Urn",                       "Lightning Urn x4",                        DS3LocationCategory.MISC),
        DS3LocationData("AP: Lightning Bolt",                      "Lightning Bolt x12",                      DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Chunk #4",                   "Titanite Chunk x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Dung Pie",                            "Dung Pie x3",                             DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Scale #2",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Soul of a Weary Warrior #2",          "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("AP: Soul of a Crestfallen Knight",        "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("AP: Titanite Chunk #5",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Ember #2",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("AP: Thunder Stoneplate Ring",             "Thunder Stoneplate Ring",                 DS3LocationCategory.RING),
        DS3LocationData("AP: Titanite Scale #3",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Ember #3",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("AP: Ancient Dragon Greatshield",          "Ancient Dragon Greatshield",              DS3LocationCategory.SHIELD),
        DS3LocationData("AP: Large Soul of a Crestfallen Knight",  "Large Soul of a Crestfallen Knight",      DS3LocationCategory.MISC),
        DS3LocationData("AP: Dragon Chaser's Ashes",               "Dragon Chaser's Ashes",                   DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("AP: Ember #4",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("AP: Dragonslayer Spear",                  "Dragonslayer Spear",                      DS3LocationCategory.WEAPON),
        DS3LocationData("AP: Dragonslayer Helm",                   "Dragonslayer Helm",                       DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Armor",                  "Dragonslayer Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Gauntlets",              "Dragonslayer Gauntlets",                  DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Dragonslayer Leggings",               "Dragonslayer Leggings",                   DS3LocationCategory.ARMOR),
        DS3LocationData("AP: Twinkling Titanite #1",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Twinkling Titanite #2",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Titanite Slab #1",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Great Magic Barrier",                 "Great Magic Barrier",                     DS3LocationCategory.SPELL,
                        hidden = True), # Hidden fall
        DS3LocationData("AP: Titanite Slab #2",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Ring of Steel Protection",            "Ring of Steel Protection",                DS3LocationCategory.RING),
        DS3LocationData("AP: Havel's Ring+1",                      "Havel's Ring+1",                          DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("AP: Covetous Gold Serpent Ring+2",        "Covetous Gold Serpent Ring+2",            DS3LocationCategory.RING,
                        ngp = True),
        DS3LocationData("AP: Titanite Scale #4",                   "Titanite Scale x3",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Twinkling Titanite #3",               "Twinkling Titanite x3",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("AP: Twinkling Dragon Torso Stone",        "Twinkling Dragon Torso Stone",            DS3LocationCategory.MISC,
                        hidden = True), # Requires gesture
        DS3LocationData("AP: Calamity Ring",                       "Calamity Ring",                           DS3LocationCategory.RING,
                        hidden = True), # Requires gesture
        DS3LocationData("AP: Twinkling Titanite #4",               "Twinkling Titanite x3",                   DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("AP: Titanite Chunk #6",                   "Titanite Chunk x6",                       DS3LocationCategory.UPGRADE,
                        miniboss = True), # Wyvern miniboss drop
        DS3LocationData("AP: Titanite Scale #5",                   "Titanite Scale x3",                       DS3LocationCategory.UPGRADE,
                        miniboss = True), # Wyvern miniboss drop
        DS3LocationData("AP: Twinkling Titanite #5",               "Twinkling Titanite x3",                   DS3LocationCategory.UPGRADE,
                        miniboss = True), # Wyvern miniboss drop
        DS3LocationData("AP: Hawkwood's Swordgrass",               "Hawkwood's Swordgrass",                   DS3LocationCategory.UNIQUE,
                        hidden = True),
        DS3LocationData("AP: Storm Curved Sword",                  "Storm Curved Sword",                      DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("AP: Dragonslayer Swordspear",             "Dragonslayer Swordspear",                 DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("AP: Lightning Storm",                     "Lightning Storm",                         DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after killing Nameless King
        DS3LocationData("AP: Golden Crown",                        "Golden Crown",                            DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AP: Dragonscale Armor",                   "Dragonscale Armor",                       DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AP: Golden Bracelets",                    "Golden Bracelets",                        DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AP: Dragonscale Waistcloth",              "Dragonscale Waistcloth",                  DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("AP: Twinkling Dragon Head Stone",         "Twinkling Dragon Head Stone",             DS3LocationCategory.UNIQUE,
                        missable = True, npc = True), # Hawkwood (quest)

        # After Oceiros's boss room, only once the Drakeblood summon in AP has been killed
        DS3LocationData("AP: Drakeblood Helm",                     "Drakeblood Helm",                         DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("AP: Drakeblood Armor",                    "Drakeblood Armor",                        DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("AP: Drakeblood Gauntlets",                "Drakeblood Gauntlets",                    DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),
        DS3LocationData("AP: Drakeblood Leggings",                 "Drakeblood Leggings",                     DS3LocationCategory.ARMOR,
                        missable = True, hostile_npc = True),

        # Appears by Stray Demon after killing Havel Knight
        DS3LocationData("AP: Havel's Helm",                        "Havel's Helm",                            DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True),
        DS3LocationData("AP: Havel's Armor",                       "Havel's Armor",                           DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True),
        DS3LocationData("AP: Havel's Gauntlets",                   "Havel's Gauntlets",                       DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True),
        DS3LocationData("AP: Havel's Leggings",                    "Havel's Leggings",                        DS3LocationCategory.ARMOR,
                        hidden = True, hostile_npc = True),
    ],
    "Kiln of the First Flame": [
        DS3LocationData("KFF: Firelink Greatsword",                "Firelink Greatsword",                     DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("KFF: Sunlight Spear",                     "Sunlight Spear",                          DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Shrine Handmaid after placing all Cinders of a Lord
        DS3LocationData("KFF: Titanite Slab",                      "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        offline = '99,0:-1:9210,110000:', hidden = True),
        DS3LocationData("KFF: Firelink Helm",                      "Firelink Helm",                           DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("KFF: Firelink Armor",                     "Firelink Armor",                          DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("KFF: Firelink Gauntlets",                 "Firelink Gauntlets",                      DS3LocationCategory.ARMOR,
                        missable = True),
        DS3LocationData("KFF: Firelink Leggings",                  "Firelink Leggings",                       DS3LocationCategory.ARMOR,
                        missable = True),

        # Yuria (quest, after Soul of Cinder)
        DS3LocationData("KFF: Billed Mask",                        "Billed Mask",                             DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("KFF: Black Dress",                        "Black Dress",                             DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("KFF: Black Gauntlets",                    "Black Gauntlets",                         DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
        DS3LocationData("KFF: Black Leggings",                     "Black Leggings",                          DS3LocationCategory.ARMOR,
                        missable = True, npc = True),
    ],

    # DLC
    "Painted World of Ariandel (Before Contraption)": [
        DS3LocationData("PW1: Valorheart",                         "Valorheart",                              DS3LocationCategory.WEAPON,
                        prominent = True, boss = True),
        DS3LocationData("PW1: Contraption Key",                    "Contraption Key",                         DS3LocationCategory.KEY,
                        prominent = True, progression = True, hostile_npc = True, key = True), # Sir Vilhelm drop
        DS3LocationData("PW1: Onyx Blade",                         "Onyx Blade",                              DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Sir Vilhelm drop
        DS3LocationData("PW: Chillbite Ring",                      "Chillbite Ring",                          DS3LocationCategory.RING,
                        npc = True), # Friede conversation
        DS3LocationData("PW1: Rime-blue Moss Clump #1",            "Rime-blue Moss Clump x2",                 DS3LocationCategory.MISC),
        DS3LocationData("PW1: Poison Gem",                         "Poison Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #1", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Follower Javelin",                   "Follower Javelin",                        DS3LocationCategory.WEAPON),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #2", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Homeward Bone #1",                   "Homeward Bone x6",                        DS3LocationCategory.MISC),
        DS3LocationData("PW1: Blessed Gem",                        "Blessed Gem",                             DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden behind a tower
        DS3LocationData("PW1: Captain's Ashes",                    "Captain's Ashes",                         DS3LocationCategory.KEY,
                        progression = True),
        DS3LocationData("PW1: Black Firebomb",                     "Black Firebomb x2",                       DS3LocationCategory.MISC),
        DS3LocationData("PW1: Shriving Stone",                     "Shriving Stone",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Millwood Greatarrow",                "Millwood Greatarrow x5",                  DS3LocationCategory.MISC),
        DS3LocationData("PW1: Millwood Greatbow",                  "Millwood Greatbow",                       DS3LocationCategory.WEAPON),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #3", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Rusted Coin #1",                     "Rusted Coin",                             DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Titanite Shard #1",            "Large Titanite Shard",                    DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #4", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Crow Quills",                        "Crow Quills",                             DS3LocationCategory.WEAPON,
                        hidden = True), # Hidden fall
        DS3LocationData("PW1: Simple Gem",                         "Simple Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #5", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Slave Knight Hood",                  "Slave Knight Hood",                       DS3LocationCategory.ARMOR),
        DS3LocationData("PW1: Slave Knight Armor",                 "Slave Knight Armor",                      DS3LocationCategory.ARMOR),
        DS3LocationData("PW1: Slave Knight Gauntlets",             "Slave Knight Gauntlets",                  DS3LocationCategory.ARMOR),
        DS3LocationData("PW1: Slave Knight Leggings",              "Slave Knight Leggings",                   DS3LocationCategory.ARMOR),
        DS3LocationData("PW1: Ember #1",                           "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("PW1: Dark Gem",                           "Dark Gem",                                DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #6", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #7", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Rusted Gold Coin",                   "Rusted Gold Coin x3",                     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Soul of a Crestfallen Knight",       "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("PW1: Way of White Corona",                "Way of White Corona",                     DS3LocationCategory.SPELL),
        DS3LocationData("PW1: Rusted Coin #2",                     "Rusted Coin x2",                          DS3LocationCategory.MISC),
        DS3LocationData("PW1: Young White Branch",                 "Young White Branch",                      DS3LocationCategory.MISC),
        DS3LocationData("PW1: Budding Green Blossom",              "Budding Green Blossom x3",                DS3LocationCategory.MISC),
        DS3LocationData("PW1: Crow Talons",                        "Crow Talons",                             DS3LocationCategory.WEAPON),
        DS3LocationData("PW1: Blood Gem",                          "Blood Gem",                               DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Hollow Gem",                         "Hollow Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Rime-blue Moss Clump #2",            "Rime-blue Moss Clump x4",                 DS3LocationCategory.MISC),
        DS3LocationData("PW1: Follower Sabre",                     "Follower Sabre",                          DS3LocationCategory.WEAPON),
        DS3LocationData("PW1: Ember #2",                           "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("PW1: Snap Freeze",                        "Snap Freeze",                             DS3LocationCategory.SPELL,
                        hidden = True), # Guaranteed drop from normal-looking Tree Woman
        DS3LocationData("PW1: Rime-blue Moss Clump #3",            "Rime-blue Moss Clump",                    DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #8", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Ember #3",                           "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("PW1: Frozen Weapon",                      "Frozen Weapon",                           DS3LocationCategory.SPELL),
        DS3LocationData("PW1: Titanite Slab",                      "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        offline = '11,0:50004700::', hidden = True), # Must kill normal-looking Tree Woman
        DS3LocationData("PW1: Homeward Bone #2",                   "Homeward Bone x2",                        DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #9", "Large Soul of an Unknown Traveler",     DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Soul of a Weary Warrior #1",   "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler #10", "Large Soul of an Unknown Traveler",    DS3LocationCategory.MISC),
        DS3LocationData("PW1: Heavy Gem",                          "Heavy Gem",                               DS3LocationCategory.UPGRADE),
        DS3LocationData("PW1: Large Soul of a Weary Warrior #2",   "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("PW1: Millwood Battle Axe",                "Millwood Battle Axe",                     DS3LocationCategory.WEAPON),
        DS3LocationData("PW1: Ethereal Oak Shield",                "Ethereal Oak Shield",                     DS3LocationCategory.SHIELD),
        DS3LocationData("PW1: Soul of a Weary Warrior",            "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("PW1: Twinkling Titanite #1",              "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW1: Large Titanite Shard #2",            "Large Titanite Shard",                    DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW1: Twinkling Titanite #2",              "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW1: Twinkling Titanite #3",              "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW1: Large Titanite Shard #3",            "Large Titanite Shard x2",                 DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW2: Champion's Bones",                   "Champion's Bones",                        DS3LocationCategory.UNIQUE,
                        offline = '11,0:50002310::', boss = True),
    ],
    "Painted World of Ariandel (After Contraption)": [
        DS3LocationData("PW2: Soul of Sister Friede",              "Soul of Sister Friede",                   DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("PW2: Titanite Slab (Friede)",             "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        offline = '11,0:50004700::', boss = True), # One-time drop after Friede Phase 2
        DS3LocationData("PW2: Floating Chaos",                     "Floating Chaos",                          DS3LocationCategory.SPELL,
                        missable = True, hostile_npc = True), # Livid Pyromancer Dunnel drop (requires ember)
        DS3LocationData("PW2: Prism Stone",                        "Prism Stone x10",                         DS3LocationCategory.MISC),
        DS3LocationData("PW2: Titanite Chunk #1",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("PW2: Titanite Chunk #2",                  "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("PW2: Follower Shield",                    "Follower Shield",                         DS3LocationCategory.SHIELD),
        DS3LocationData("PW2: Large Titanite Shard #1",            "Large Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("PW2: Quakestone Hammer",                  "Quakestone Hammer",                       DS3LocationCategory.WEAPON),
        DS3LocationData("PW2: Ember",                              "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("PW2: Large Titanite Shard #2",            "Large Titanite Shard x2",                 DS3LocationCategory.UPGRADE),
        DS3LocationData("PW2: Soul of a Crestfallen Knight #1",    "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("PW2: Soul of a Crestfallen Knight #2",    "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("PW2: Large Soul of a Crestfallen Knight", "Large Soul of a Crestfallen Knight",      DS3LocationCategory.MISC),
        DS3LocationData("PW2: Earth Seeker",                       "Earth Seeker",                            DS3LocationCategory.WEAPON),
        DS3LocationData("PW2: Follower Torch",                     "Follower Torch",                          DS3LocationCategory.SHIELD),
        DS3LocationData("PW2: Dung Pie",                           "Dung Pie x2",                             DS3LocationCategory.MISC),
        DS3LocationData("PW2: Vilhelm's Helm",                     "Vilhelm's Helm",                          DS3LocationCategory.ARMOR),
        DS3LocationData("PW2: Vilhelm's Armor",                    "Vilhelm's Armor",                         DS3LocationCategory.ARMOR),
        DS3LocationData("PW2: Vilhelm's Gauntlets",                "Vilhelm's Gauntlets",                     DS3LocationCategory.ARMOR),
        DS3LocationData("PW2: Vilhelm's Leggings",                 "Vilhelm's Leggings",                      DS3LocationCategory.ARMOR),
        DS3LocationData("PW2: Pyromancer's Parting Flame",         "Pyromancer's Parting Flame",              DS3LocationCategory.WEAPON,
                        hidden = True), # Behind illusory wall
        DS3LocationData("PW2: Homeward Bone",                      "Homeward Bone x2",                        DS3LocationCategory.MISC,
                        hidden = True), # Behind illusory wall
        DS3LocationData("PW2: Twinkling Titanite #1",              "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW2: Twinkling Titanite #2",              "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("PW2: Friede's Great Scythe",              "Friede's Great Scythe",                   DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("PW2: Rose of Ariandel",                   "Rose of Ariandel",                        DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("PW2: Titanite Slab (Corvian)",            "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        offline = '11,0:50006540::', missable = True, npc = True), # Corvian Settler (quest)

        # Shrine Handmaid after killing Sister Friede
        DS3LocationData("PW2: Ordained Hood",                      "Ordained Hood",                           DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("PW2: Ordained Dress",                     "Ordained Dress",                          DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
        DS3LocationData("PW2: Ordained Trousers",                  "Ordained Trousers",                       DS3LocationCategory.ARMOR,
                        boss = True, shop = True),
    ],
    "Dreg Heap": [
        DS3LocationData("DH: Soul of the Demon Prince",            "Soul of the Demon Prince",                DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("DH: Siegbräu",                            "Siegbräu",                                DS3LocationCategory.MISC,
                        missable = True, npc = True), # Lapp (quest or kill)
        DS3LocationData("DH: Flame Fan",                           "Flame Fan",                               DS3LocationCategory.SPELL,
                        hostile_npc = True), # Desert Pyromancer Zoey drop
        DS3LocationData("DH: Ember #1",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("DH: Soul of a Weary Warrior",             "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("DH: Titanite Chunk #1",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Aquamarine Dagger",                   "Aquamarine Dagger",                       DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Twinkling Titanite #1",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Murky Hand Scythe",                   "Murky Hand Scythe",                       DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Divine Blessing #1",                  "Divine Blessing",                         DS3LocationCategory.MISC),
        DS3LocationData("DH: Ring of Steel Protection+3",          "Ring of Steel Protection+3",              DS3LocationCategory.RING),
        DS3LocationData("DH: Soul of a Crestfallen Knight",        "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("DH: Rusted Coin",                         "Rusted Coin x2",                          DS3LocationCategory.MISC),
        DS3LocationData("DH: Titanite Chunk #2",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Murky Longstaff",                     "Murky Longstaff",                         DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Ember #2",                            "Ember",                                   DS3LocationCategory.MISC,
                        hidden = True), # Behind illusory wall
        DS3LocationData("DH: Great Soul Dregs",                    "Great Soul Dregs",                        DS3LocationCategory.SPELL,
                        hidden = True), # Behind illusory wall
        DS3LocationData("DH: Covetous Silver Serpent Ring+3",      "Covetous Silver Serpent Ring+3",          DS3LocationCategory.RING,
                        hidden = True), # Behind illusory wall
        DS3LocationData("DH: Titanite Chunk #3",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Homeward Bone #1",                    "Homeward Bone x3",                        DS3LocationCategory.MISC),
        DS3LocationData("DH: Lightning Urn",                       "Lightning Urn x4",                        DS3LocationCategory.MISC),
        DS3LocationData("DH: Projected Heal",                      "Projected Heal",                          DS3LocationCategory.SPELL),
        DS3LocationData("DH: Large Soul of a Weary Warrior #1",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("DH: Lothric War Banner",                  "Lothric War Banner",                      DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Titanite Scale #1",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Black Firebomb",                      "Black Firebomb x4",                       DS3LocationCategory.MISC),
        DS3LocationData("DH: Titanite Chunk #4",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Twinkling Titanite #2",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Desert Pyromancer Garb",              "Desert Pyromancer Garb",                  DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Titanite Chunk #5",                   "Titanite Chunk x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Giant Door Shield",                   "Giant Door Shield",                       DS3LocationCategory.SHIELD),
        DS3LocationData("DH: Ember #3",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("DH: Desert Pyromancer Gloves",            "Desert Pyromancer Gloves",                DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Desert Pyromancer Skirt",             "Desert Pyromancer Skirt",                 DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Titanite Scale #2",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Purple Moss Clump",                   "Purple Moss Clump x4",                    DS3LocationCategory.MISC),
        DS3LocationData("DH: Ring of Favor+3",                     "Ring of Favor+3",                         DS3LocationCategory.RING),
        DS3LocationData("DH: Titanite Chunk #6",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Large Soul of a Weary Warrior #2",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("DH: Titanite Slab",                       "Titanite Slab",                           DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Titanite Chunk #7",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Loincloth",                           "Loincloth",                               DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Titanite Chunk #8",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("DH: Large Soul of a Weary Warrior #3",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("DH: Harald Curved Greatsword",            "Harald Curved Greatsword",                DS3LocationCategory.WEAPON),
        DS3LocationData("DH: Homeward Bone #2",                    "Homeward Bone",                           DS3LocationCategory.MISC),
        DS3LocationData("DH: Prism Stone",                         "Prism Stone x6",                          DS3LocationCategory.MISC),
        DS3LocationData("DH: Desert Pyromancer Hood",              "Desert Pyromancer Hood",                  DS3LocationCategory.ARMOR),
        DS3LocationData("DH: Twinkling Titanite #3",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("DH: Divine Blessing #2",                  "Divine Blessing",                         DS3LocationCategory.MISC),
        DS3LocationData("DH: Ember #4",                            "Ember",                                   DS3LocationCategory.MISC,
                        hidden = True), # Hidden fall
        DS3LocationData("DH: Small Envoy Banner",                  "Small Envoy Banner",                      DS3LocationCategory.KEY,
                        progression = True, boss = True),
        DS3LocationData("DH: Twinkling Titanite #4",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall, also guaranteed drop from killing normal-looking pilgrim
        DS3LocationData("DH: Twinkling Titanite #5",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall, also guaranteed drop from killing normal-looking pilgrim
        DS3LocationData("DH: Twinkling Titanite #6",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from killing normal-looking pilgrim
        DS3LocationData("DH: Demon's Scar",                        "Demon's Scar",                            DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("DH: Seething Chaos",                      "Seething Chaos",                          DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),

        # Stone-humped Hag's shop
        DS3LocationData("DH: Splitleaf Greatsword",                "Splitleaf Greatsword",                    DS3LocationCategory.WEAPON,
                        shop = True),
        DS3LocationData("DH: Divine Blessing #3",                  "Divine Blessing",                         DS3LocationCategory.MISC,
                        shop = True),
        DS3LocationData("DH: Hidden Blessing",                     "Hidden Blessing",                         DS3LocationCategory.MISC,
                        shop = True),
        DS3LocationData("DH: Rusted Gold Coin",                    "Rusted Gold Coin",                        DS3LocationCategory.MISC,
                        shop = True),
        DS3LocationData("DH: Ember #5",                            "Ember",                                   DS3LocationCategory.MISC,
                        shop = True),
    ],
    "Ringed City": [
        DS3LocationData("RC: Titanite Slab #1",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        prominent = True, boss = True), # Halflight drop, only once
        DS3LocationData("RC: Soul of Darkeater Midir",             "Soul of Darkeater Midir",                 DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("RC: Sacred Chime of Filianore",           "Sacred Chime of Filianore",               DS3LocationCategory.WEAPON,
                        npc = True), # Shira (kill or quest)
        DS3LocationData("RC: Titanite Slab #2",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        npc = True), # Shira (kill or quest)
        DS3LocationData("RC: Crucifix of the Mad King",            "Crucifix of the Mad King",                DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Shira drop
        DS3LocationData("RC: Ledo's Great Hammer",                 "Ledo's Great Hammer",                     DS3LocationCategory.WEAPON,
                        hostile_npc = True), # Silver Knight Ledo drop
        DS3LocationData("RC: Wolf Ring+3",                         "Wolf Ring+3",                             DS3LocationCategory.RING,
                        hostile_npc = True), # Alva drop
        DS3LocationData("RC: Blindfold Mask",                      "Blindfold Mask",                          DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Moaning Knight drop
        DS3LocationData("RC: Titanite Scale #1",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Ruin Helm",                           "Ruin Helm",                               DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Armor",                          "Ruin Armor",                              DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Gauntlets",                      "Ruin Gauntlets",                          DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Ruin Leggings",                       "Ruin Leggings",                           DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Budding Green Blossom #1",            "Budding Green Blossom x2",                DS3LocationCategory.MISC),
        DS3LocationData("RC: Titanite Chunk #1",                   "Titanite Chunk x2",                       DS3LocationCategory.MISC),
        DS3LocationData("RC: Ember #1",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("RC: Budding Green Blossom #2",            "Budding Green Blossom x2",                DS3LocationCategory.MISC),
        DS3LocationData("RC: Hidden Blessing #1",                  "Hidden Blessing",                         DS3LocationCategory.MISC),
        DS3LocationData("RC: Soul of a Crestfallen Knight #1",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("RC: Large Soul of a Weary Warrior #1",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("RC: Ember #2",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("RC: Purging Stone",                       "Purging Stone x2",                        DS3LocationCategory.MISC),
        DS3LocationData("RC: Hollow Gem",                          "Hollow Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Titanite Chunk #2",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Twinkling Titanite #1",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("RC: Shriving Stone",                      "Shriving Stone",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Shira's Crown",                       "Shira's Crown",                           DS3LocationCategory.ARMOR,
                        hidden = True), # Have to return to a cleared area
        DS3LocationData("RC: Shira's Armor",                       "Shira's Armor",                           DS3LocationCategory.ARMOR,
                        hidden = True), # Have to return to a cleared area
        DS3LocationData("RC: Shira's Gloves",                      "Shira's Gloves",                          DS3LocationCategory.ARMOR,
                        hidden = True), # Have to return to a cleared area
        DS3LocationData("RC: Shira's Trousers",                    "Shira's Trousers",                        DS3LocationCategory.ARMOR,
                        hidden = True), # Have to return to a cleared area
        DS3LocationData("RC: Mossfruit #1",                        "Mossfruit x2",                            DS3LocationCategory.MISC),
        DS3LocationData("RC: Large Soul of a Crestfallen Knight #1", "Large Soul of a Crestfallen Knight",    DS3LocationCategory.MISC),
        DS3LocationData("RC: Ringed Knight Spear",                 "Ringed Knight Spear",                     DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Black Witch Hat",                     "Black Witch Hat",                         DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Alva
        DS3LocationData("RC: Black Witch Garb",                    "Black Witch Garb",                        DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Alva
        DS3LocationData("RC: Black Witch Wrappings",               "Black Witch Wrappings",                   DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Alva
        DS3LocationData("RC: Black Witch Trousers",                "Black Witch Trousers",                    DS3LocationCategory.ARMOR,
                        hostile_npc = True), # Alva
        DS3LocationData("RC: Dragonhead Shield",                   "Dragonhead Shield",                       DS3LocationCategory.SHIELD,
                        hidden = True), # "Show Your Humanity" puzzle
        DS3LocationData("RC: Titanite Chunk #3",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE,
                        hidden = True), # Hidden fall
        DS3LocationData("RC: Mossfruit #2",                        "Mossfruit x2",                            DS3LocationCategory.MISC),
        DS3LocationData("RC: Large Soul of a Crestfallen Knight #2", "Large Soul of a Crestfallen Knight",    DS3LocationCategory.MISC,
                        hidden = True), # "Show Your Humanity" puzzle
        DS3LocationData("RC: Covetous Gold Serpent Ring+3",        "Covetous Gold Serpent Ring+3",            DS3LocationCategory.RING),
        DS3LocationData("RC: Titanite Chunk #4",                   "Titanite Chunk x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Dark Gem",                            "Dark Gem",                                DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Prism Stone",                         "Prism Stone x4",                          DS3LocationCategory.MISC),
        DS3LocationData("RC: Ringed Knight Straight Sword",        "Ringed Knight Straight Sword",            DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Havel's Ring+3",                      "Havel's Ring+3",                          DS3LocationCategory.RING,
                        hidden = True), # Hidden fall
        DS3LocationData("RC: Titanite Chunk #5",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Twinkling Titanite #2",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Soul of a Weary Warrior #1",          "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("RC: Preacher's Right Arm",                "Preacher's Right Arm",                    DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Rubbish #1",                          "Rubbish",                                 DS3LocationCategory.MISC),
        DS3LocationData("RC: Titanite Chunk #6",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Black Witch Veil",                    "Black Witch Veil",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Twinkling Titanite #3",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Soul of a Crestfallen Knight #2",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("RC: White Preacher Head",                 "White Preacher Head",                     DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Titanite Scale #2",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Titanite Scale #3",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Dragonhead Greatshield",              "Dragonhead Greatshield",                  DS3LocationCategory.SHIELD),
        DS3LocationData("RC: Titanite Scale #4",                   "Titanite Scale x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Rubbish #2",                          "Rubbish",                                 DS3LocationCategory.MISC),
        DS3LocationData("RC: Large Soul of a Weary Warrior #2",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("RC: Titanite Scale #5",                   "Titanite Scale x2",                       DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Titanite Scale #6",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Lightning Gem",                       "Lightning Gem",                           DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Blessed Gem",                         "Blessed Gem",                             DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Simple Gem",                          "Simple Gem",                              DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Large Soul of a Weary Warrior #3",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("RC: Lightning Arrow",                     "Lightning Arrow",                         DS3LocationCategory.SPELL),
        DS3LocationData("RC: Chloranthy Ring+3",                   "Chloranthy Ring+3",                       DS3LocationCategory.RING,
                        hidden = True), # Hidden fall
        DS3LocationData("RC: Ember #3",                            "Ember",                                   DS3LocationCategory.MISC),
        DS3LocationData("RC: Filianore's Spear Ornament",          "Filianore's Spear Ornament",              DS3LocationCategory.MISC,
                        offline = '13,0:55100700::'),
        DS3LocationData("RC: Antiquated Plain Garb",               "Antiquated Plain Garb",                   DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Violet Wrappings",                    "Violet Wrappings",                        DS3LocationCategory.ARMOR),
        DS3LocationData("RC: Soul of a Weary Warrior #2",          "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("RC: Twinkling Titanite #4",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Budding Green Blossom #3",            "Budding Green Blossom x3",                DS3LocationCategory.MISC),
        DS3LocationData("RC: Titanite Chunk #7",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Large Soul of a Weary Warrior #4",    "Large Soul of a Weary Warrior",           DS3LocationCategory.MISC),
        DS3LocationData("RC: Soul of a Weary Warrior #3",          "Soul of a Weary Warrior",                 DS3LocationCategory.MISC),
        DS3LocationData("RC: Titanite Scale #7",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Soul of a Crestfallen Knight #3",     "Soul of a Crestfallen Knight",            DS3LocationCategory.MISC),
        DS3LocationData("RC: White Birch Bow",                     "White Birch Bow",                         DS3LocationCategory.WEAPON),
        DS3LocationData("RC: Titanite Chunk #8",                   "Titanite Chunk",                          DS3LocationCategory.UPGRADE),
        DS3LocationData("RC: Young White Branch #1",               "Young White Branch",                      DS3LocationCategory.MISC),
        DS3LocationData("RC: Young White Branch #2",               "Young White Branch",                      DS3LocationCategory.MISC),
        DS3LocationData("RC: Young White Branch #3",               "Young White Branch",                      DS3LocationCategory.MISC),
        DS3LocationData("RC: Ringed Knight Paired Greatswords",    "Ringed Knight Paired Greatswords",        DS3LocationCategory.WEAPON,
                        hidden = True), # Guaranteed drop from a normal-looking Ringed Knight
        DS3LocationData("RC: Hidden Blessing #2",                  "Hidden Blessing",                         DS3LocationCategory.MISC,
                        miniboss = True), # Judicator drop
        DS3LocationData("RC: Divine Blessing #1",                  "Divine Blessing",                         DS3LocationCategory.MISC,
                        miniboss = True), # Judicator drop
        DS3LocationData("RC: Divine Blessing #2",                  "Divine Blessing",                         DS3LocationCategory.MISC,
                        miniboss = True, hidden = True), # Judicator drop, "Show Your Humanity" puzzle
        DS3LocationData("RC: Ring of the Evil Eye+3",              "Ring of the Evil Eye+3",                  DS3LocationCategory.RING,
                        mimic = True, hidden = True), # Hidden fall
        DS3LocationData("RC: Iron Dragonslayer Helm",              "Iron Dragonslayer Helm",                  DS3LocationCategory.ARMOR,
                        miniboss = True),
        DS3LocationData("RC: Iron Dragonslayer Armor",             "Iron Dragonslayer Armor",                 DS3LocationCategory.ARMOR,
                        miniboss = True),
        DS3LocationData("RC: Iron Dragonslayer Gauntlets",         "Iron Dragonslayer Gauntlets",             DS3LocationCategory.ARMOR,
                        miniboss = True),
        DS3LocationData("RC: Iron Dragonslayer Leggings",          "Iron Dragonslayer Leggings",              DS3LocationCategory.ARMOR,
                        miniboss = True),
        DS3LocationData("RC: Church Guardian Shiv",                "Church Guardian Shiv",                    DS3LocationCategory.MISC),
        DS3LocationData("RC: Spears of the Church",                "Spears of the Church",                    DS3LocationCategory.UNIQUE,
                        boss = True), # Midir drop
        DS3LocationData("RC: Ritual Spear Fragment",               "Ritual Spear Fragment",                   DS3LocationCategory.UNIQUE),
        DS3LocationData("RC: Titanite Scale #8",                   "Titanite Scale",                          DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Twinkling Titanite #5",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Titanite Scale #9",                   "Titanite Scale x2",                       DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Twinkling Titanite #6",               "Twinkling Titanite x2",                   DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Titanite Scale #10",                  "Titanite Scale",                          DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Twinkling Titanite #7",               "Twinkling Titanite",                      DS3LocationCategory.UPGRADE,
                        lizard = True),
        DS3LocationData("RC: Soul of Slave Knight Gael",           "Soul of Slave Knight Gael",               DS3LocationCategory.BOSS,
                        prominent = True, boss = True),
        DS3LocationData("RC: Blood of the Dark Soul",              "Blood of the Dark Soul",                  DS3LocationCategory.KEY),
        DS3LocationData("RC: Titanite Slab #3",                    "Titanite Slab",                           DS3LocationCategory.UPGRADE,
                        hidden = True), # Guaranteed drop from normal-looking Ringed Knight
        DS3LocationData("RC: Frayed Blade",                        "Frayed Blade",                            DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RC: Old Moonlight",                       "Old Moonlight",                           DS3LocationCategory.SPELL,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RC: Gael's Greatsword",                   "Gael's Greatsword",                       DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),
        DS3LocationData("RC: Repeating Crossbow",                  "Repeating Crossbow",                      DS3LocationCategory.WEAPON,
                        missable = True, boss = True, shop = True),

        # Lapp 
        DS3LocationData("RC: Siegbräu",                            "Siegbräu",                                DS3LocationCategory.MISC,
                        missable = True, npc = True), # Lapp (quest)
        # Quest or Shrine Handmaiden after death
        DS3LocationData("RC: Lapp's Helm",                         "Lapp's Helm",                             DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RC: Lapp's Armor",                        "Lapp's Armor",                            DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RC: Lapp's Gauntlets",                    "Lapp's Gauntlets",                        DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
        DS3LocationData("RC: Lapp's Leggings",                     "Lapp's Leggings",                         DS3LocationCategory.ARMOR,
                        missable = True, npc = True, shop = True),
    ],

    # Unlockable shops. We only bother creating a "region" for these for shops that are locked
    # behind keys and always have items available either through the shop or through the NPC's
    # ashes.
    "Greirat's Shop": [
        DS3LocationData("Greirat: Blue Tearstone Ring",            "Blue Tearstone Ring",               DS3LocationCategory.RING,
                        offline = '01,0:50006120::', npc = True),
        DS3LocationData("Greirat: Ember #1",                       "Ember",                             DS3LocationCategory.MISC,
                        offline = "99,0:-1:110000,120000,70000110:", shop = True, npc = True),

        # Undead Settlement rewards
        DS3LocationData("Greirat: Divine Blessing #1",             "Divine Blessing",                   DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,120000,70000150,70000175:', missable = True, shop = True, npc = True),
        DS3LocationData("Greirat: Ember #2",                       "Ember",                             DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,120000,70000150,70000175:', missable = True, shop = True, npc = True),

        # Irityhll rewards
        DS3LocationData("Greirat: Divine Blessing #2",             "Divine Blessing",                   DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,120000,70000151,70000176:', missable = True, shop = True, npc = True),
        DS3LocationData("Greirat: Hidden Blessing",                "Hidden Blessing",                   DS3LocationCategory.MISC,
                        offline = '99,0:-1:110000,120000,70000151,70000176:', missable = True, shop = True, npc = True),
        DS3LocationData("Greirat: Titanite Scale",                 "Titanite Scale",                    DS3LocationCategory.UPGRADE,
                        offline = '99,0:-1:110000,120000,70000151,70000176:', missable = True, shop = True, npc = True),
        DS3LocationData("Greirat: Twinkling Titanite",            "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        offline = '99,0:-1:110000,120000,70000151,70000176:', missable = True, shop = True, npc = True),

        # Lothric rewards (from Shrine Handmaid)
        DS3LocationData("Greirat: Ember #3",                       "Twinkling Titanite",                DS3LocationCategory.UPGRADE,
                        offline = '99,0:-1:110000,120000,70000152,70000177:', missable = True, shop = True, npc = True),
    ],
    "Karla's Shop": [
        DS3LocationData("Karla: Affinity",                         "Affinity",                          DS3LocationCategory.SPELL,
                        shop = True, npc = True),
        DS3LocationData("Karla: Dark Edge",                        "Dark Edge",                         DS3LocationCategory.SPELL,
                        shop = True, npc = True),

        # Quelana Pyromancy Tome
        DS3LocationData("Karla: Firestorm",                        "Firestorm",                         DS3LocationCategory.SPELL,
                        missable = True, shop = True, npc = True),
        DS3LocationData("Karla: Rapport",                          "Rapport",                           DS3LocationCategory.SPELL,
                        missable = True, shop = True, npc = True),
        DS3LocationData("Karla: Fire Whip",                        "Fire Whip",                         DS3LocationCategory.SPELL,
                        missable = True, shop = True, npc = True),

        # Grave Warden Pyromancy Tome
        DS3LocationData("Karla: Black Flame",                      "Black Flame",                       DS3LocationCategory.SPELL,
                        missable = True, shop = True, npc = True),
        DS3LocationData("Karla: Black Fire Orb",                   "Black Fire Orb",                    DS3LocationCategory.SPELL,
                        missable = True, shop = True, npc = True),
 
        # Drops on death. Missable because the player would have to decide between killing her or
        # seeing everything she sells.
        DS3LocationData("Karla: Karla's Pointed Hat",              "Karla's Pointed Hat",               DS3LocationCategory.ARMOR,
                        offline = '07,0:50006150::', missable = True, npc = True),
        DS3LocationData("Karla: Karla's Coat",                     "Karla's Coat",                      DS3LocationCategory.ARMOR,
                        offline = '07,0:50006150::', missable = True, npc = True),
        DS3LocationData("Karla: Karla's Gloves",                   "Karla's Gloves",                    DS3LocationCategory.ARMOR,
                        offline = '07,0:50006150::', missable = True, npc = True),
        DS3LocationData("Karla: Karla's Trousers",                 "Karla's Trousers",                  DS3LocationCategory.ARMOR,
                        offline = '07,0:50006150::', missable = True, npc = True),
    ],
}


for region in [
    "Painted World of Ariandel (Before Contraption)",
    "Painted World of Ariandel (After Contraption)",
    "Dreg Heap",
    "Ringed City",
]:
    for location in location_tables[region]:
        location.dlc = True


location_name_groups: Dict[str, Set[str]] = {
    # We could insert these locations automatically with setdefault(), but we set them up explicitly
    # instead so we can choose the ordering.
    "Prominent": set(),
    "Progression": set(),
    "Boss Rewards": set(),
    "Miniboss Rewards": set(),
    "Mimic Rewards": set(),
    "Hostile NPC Rewards": set(),
    "Small Crystal Lizards": set(),
    "Keys": set(),
    "Upgrade": set(),
    "Miscellaneous": set(),
    "Hidden": set()
}


location_dictionary: Dict[str, DS3LocationData] = {}
for location_name, location_table in location_tables.items():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})

    for location_data in location_table:
        for group_name in location_data.location_groups():
            location_name_groups[group_name].add(location_data.name)

    # Allow entire locations to be added to location sets.
    if not location_name.endswith(" Shop"):
        location_name_groups[location_name] = frozenset([
            location_data.name for location_data in location_table
        ])

location_name_groups["Painted World of Ariandel"] = (
    location_name_groups["Painted World of Ariandel (Before Contraption)"]
        .union(location_name_groups["Painted World of Ariandel (After Contraption)"])
)
del location_name_groups["Painted World of Ariandel (Before Contraption)"]
del location_name_groups["Painted World of Ariandel (After Contraption)"]

location_name_groups["DLC"] = (
    location_name_groups["Painted World of Ariandel"]
        .union(location_name_groups["Dreg Heap"])
        .union(location_name_groups["Ringed City"])
)
