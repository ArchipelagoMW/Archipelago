from typing import cast, ClassVar, Optional, Dict, List, Set
from dataclasses import dataclass

from BaseClasses import ItemClassification, Location, Region
from .Items import DS3ItemCategory, item_dictionary

# Regions in approximate order of reward, mostly measured by how high-quality the upgrade items are
# in each region.
region_order = [
    "Cemetery of Ash",
    "Firelink Shrine",
    "High Wall of Lothric",
    "Greirat's Shop",
    "Undead Settlement",
    "Road of Sacrifices",
    "Farron Keep",
    "Cathedral of the Deep",
    "Catacombs of Carthus",
    "Smouldering Lake",
    "Irithyll of the Boreal Valley",
    "Irithyll Dungeon",
    "Karla's Shop",
    # The first half of Painted World has one Titanite Slab but mostly Large Titanite Shards,
    # much like Irithyll Dungeon.
    "Painted World of Ariandel (Before Contraption)",
    "Anor Londo",
    "Profaned Capital",
    # The second half of Painted World has two Titanite Chunks and two Titanite Slabs, which
    # puts it on the low end of the post-Lothric Castle areas in terms of rewards.
    "Painted World of Ariandel (After Contraption)",
    "Lothric Castle",
    "Consumed King's Garden",
    "Untended Graves",
    # List this late because it contains a Titanite Slab in the base game
    "Firelink Shrine Bell Tower",
    "Grand Archives",
    "Archdragon Peak",
    "Kiln of the First Flame",
    # Both areas of DLC2 have premium rewards.
    "Dreg Heap",
    "Ringed City",
]


@dataclass
class DS3LocationData:
    __location_id: ClassVar[int] = 100000
    """The next location ID to use when creating location data."""

    name: str
    """The name of this location according to Archipelago.

    This needs to be unique within this world."""

    default_item_name: Optional[str]
    """The name of the item that appears by default in this location.

    If this is None, that indicates that this location is an "event" that's
    automatically considered accessed as soon as it's available. Events are used
    to indicate major game transitions that aren't otherwise gated by items so
    that progression balancing and item smoothing is more accurate for DS3.
    """

    ap_code: Optional[int] = None
    """Archipelago's internal ID for this location (also known as its "address")."""

    region_value: int = 0
    """The relative value of items in this location's region.

    This is used to sort locations when placing items like the base game.
    """

    static: Optional[str] = None
    """The key in the static randomizer's Slots table that corresponds to this location.

    By default, the static randomizer chooses its location based on the region and the item name.
    If the item name is unique across the whole game, it can also look it up based on that alone. If
    there are multiple instances of the same item type in the same region, it will assume its order
    (in annotations.txt) matches Archipelago's order.

    In cases where this heuristic doesn't work, such as when Archipelago's region categorization or
    item name disagrees with the static randomizer's, this field is used to provide an explicit
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

    drop: bool = False
    """Whether this is an item dropped by a (non-boss) enemy.

    This is automatically set to True if miniboss, mimic, lizard, or hostile_npc is True.
    """

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
    """Whether this location can appear in an NPC's shop.

    Items like Lapp's Set which can appear both in the overworld and in a shop
    should still be tagged as shop.
    """

    conditional: bool = False
    """Whether this location is conditional on a progression item.

    This is used to track locations that won't become available until an unknown amount of time into
    the run, and as such shouldn't have "similar to the base game" items placed in them.
    """

    hidden: bool = False
    """Whether this location is particularly tricky to find.

    This is for players without an encyclopedic knowledge of DS3 who don't want to get stuck looking
    for an illusory wall or one random mob with a guaranteed drop.
    """

    @property
    def is_event(self) -> bool:
        """Whether this location represents an event rather than a specific item pickup."""
        return self.default_item_name is None

    def __post_init__(self):
        if not self.is_event:
            self.ap_code = self.ap_code or DS3LocationData.__location_id
            DS3LocationData.__location_id += 1
        if self.miniboss or self.mimic or self.lizard or self.hostile_npc: self.drop = True

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
        if self.npc: names.append("Friendly NPC Rewards")
        if self.lizard: names.append("Small Crystal Lizards")
        if self.hidden: names.append("Hidden")

        default_item = item_dictionary[cast(str, self.default_item_name)]
        names.append({
                         DS3ItemCategory.WEAPON_UPGRADE_5: "Weapons",
                         DS3ItemCategory.WEAPON_UPGRADE_10: "Weapons",
                         DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE: "Weapons",
                         DS3ItemCategory.SHIELD: "Shields",
                         DS3ItemCategory.SHIELD_INFUSIBLE: "Shields",
                         DS3ItemCategory.ARMOR: "Armor",
                         DS3ItemCategory.RING: "Rings",
                         DS3ItemCategory.SPELL: "Spells",
                         DS3ItemCategory.MISC: "Miscellaneous",
                         DS3ItemCategory.UNIQUE: "Unique",
                         DS3ItemCategory.BOSS: "Boss Souls",
                         DS3ItemCategory.SOUL: "Small Souls",
                         DS3ItemCategory.UPGRADE: "Upgrade",
                         DS3ItemCategory.HEALING: "Healing",
                     }[default_item.category])
        if default_item.classification == ItemClassification.progression:
            names.append("Progression")

        return names


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"
    data: DS3LocationData

    def __init__(
            self,
            player: int,
            data: DS3LocationData,
            parent: Optional[Region] = None,
            event: bool = False):
        super().__init__(player, data.name, None if event else data.ap_code, parent)
        self.data = data


# Naming conventions:
#
# * The regions in item names should match the physical region where the item is
#   acquired, even if its logical region is different. For example, Irina's
#   inventory appears in the "Undead Settlement" region because she's not
#   accessible until there, but it begins with "FS:" because that's where her
#   items are purchased.
#
# * Avoid using vanilla enemy placements as landmarks, because these are
#   randomized by the enemizer by default. Instead, use generic terms like
#   "mob", "boss", and "miniboss".
#
# * Location descriptions don't need to direct the player to the precise spot.
#   You can assume the player is broadly familiar with Dark Souls III or willing
#   to look at a vanilla guide. Just give a general area to look in or an idea
#   of what quest a check is connected to. Terseness is valuable: try to keep
#   each location description short enough that the whole line doesn't exceed
#   100 characters.
#
# * Use "[name] drop" for items that require killing an NPC who becomes hostile
#   as part of their normal quest, "kill [name]" for items that require killing
#   them even when they aren't hostile, and just "[name]" for items that are
#   naturally available as part of their quest.
location_tables: Dict[str, List[DS3LocationData]] = {
    "Cemetery of Ash": [
        DS3LocationData("CA: Soul of a Deserted Corpse - right of spawn",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("CA: Firebomb - down the cliff edge", "Firebomb x5"),
        DS3LocationData("CA: Titanite Shard - jump to coffin", "Titanite Shard"),
        DS3LocationData("CA: Soul of an Unknown Traveler - by miniboss",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("CA: Speckled Stoneplate Ring+1 - by miniboss",
                        "Speckled Stoneplate Ring+1", ngp=True),
        DS3LocationData("CA: Titanite Scale - miniboss drop", "Titanite Scale", miniboss=True),
        DS3LocationData("CA: Coiled Sword - boss drop", "Coiled Sword", prominent=True,
                        progression=True, boss=True),
    ],
    "Firelink Shrine": [
        # Ludleth drop, does not permanently die
        DS3LocationData("FS: Skull Ring - kill Ludleth", "Skull Ring", hidden=True, drop=True,
                        npc=True),

        # Sword Master drops
        DS3LocationData("FS: Uchigatana - NPC drop", "Uchigatana", hostile_npc=True),
        DS3LocationData("FS: Master's Attire - NPC drop", "Master's Attire", hostile_npc=True),
        DS3LocationData("FS: Master's Gloves - NPC drop", "Master's Gloves", hostile_npc=True),

        DS3LocationData("FS: Broken Straight Sword - gravestone after boss",
                        "Broken Straight Sword"),
        DS3LocationData("FS: Homeward Bone - cliff edge after boss", "Homeward Bone"),
        DS3LocationData("FS: Ember - path right of Firelink entrance", "Ember"),
        DS3LocationData("FS: Soul of a Deserted Corpse - bell tower door",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("FS: East-West Shield - tree by shrine entrance", "East-West Shield"),
        DS3LocationData("FS: Homeward Bone - path above shrine entrance", "Homeward Bone"),
        DS3LocationData("FS: Ember - above shrine entrance", "Ember"),
        DS3LocationData("FS: Wolf Ring+2 - left of boss room exit", "Wolf Ring+2", ngp=True),
        # Leonhard (quest)
        DS3LocationData("FS: Cracked Red Eye Orb - Leonhard", "Cracked Red Eye Orb x5",
                        missable=True, npc=True),
        # Leonhard (kill or quest), missable because he can disappear sometimes
        DS3LocationData("FS: Lift Chamber Key - Leonhard", "Lift Chamber Key", missable=True,
                        npc=True, drop=True),

        # Shrine Handmaid shop
        DS3LocationData("FS: White Sign Soapstone - shop", "White Sign Soapstone", shop=True),
        DS3LocationData("FS: Dried Finger - shop", "Dried Finger", shop=True),
        DS3LocationData("FS: Tower Key - shop", "Tower Key", progression=True, shop=True),
        DS3LocationData("FS: Ember - shop", "Ember", static='99,0:-1:110000:', shop=True),
        DS3LocationData("FS: Farron Dart - shop", "Farron Dart", static='99,0:-1:110000:',
                        shop=True),
        DS3LocationData("FS: Soul Arrow - shop", "Soul Arrow", static='99,0:-1:110000:',
                        shop=True),
        DS3LocationData("FS: Heal Aid - shop", "Heal Aid", shop=True),
        DS3LocationData("FS: Alluring Skull - Mortician's Ashes", "Alluring Skull", shop=True,
                        conditional=True),
        DS3LocationData("FS: Ember - Mortician's Ashes", "Ember",
                        static='99,0:-1:110000,70000100:', shop=True, conditional=True),
        DS3LocationData("FS: Grave Key - Mortician's Ashes", "Grave Key", shop=True,
                        conditional=True),
        DS3LocationData("FS: Life Ring - Dreamchaser's Ashes", "Life Ring", shop=True,
                        conditional=True),
        # Only if you say where the ashes were found
        DS3LocationData("FS: Hidden Blessing - Dreamchaser's Ashes", "Hidden Blessing",
                        missable=True, shop=True),
        DS3LocationData("FS: Lloyd's Shield Ring - Paladin's Ashes", "Lloyd's Shield Ring",
                        shop=True, conditional=True),
        DS3LocationData("FS: Ember - Grave Warden's Ashes", "Ember",
                        static='99,0:-1:110000,70000103:', shop=True, conditional=True),
        # Prisoner Chief's Ashes
        DS3LocationData("FS: Karla's Pointed Hat - Prisoner Chief's Ashes", "Karla's Pointed Hat",
                        static='99,0:-1:110000,70000105:', shop=True, conditional=True),
        DS3LocationData("FS: Karla's Coat - Prisoner Chief's Ashes", "Karla's Coat",
                        static='99,0:-1:110000,70000105:', shop=True, conditional=True),
        DS3LocationData("FS: Karla's Gloves - Prisoner Chief's Ashes", "Karla's Gloves",
                        static='99,0:-1:110000,70000105:', shop=True, conditional=True),
        DS3LocationData("FS: Karla's Trousers - Prisoner Chief's Ashes", "Karla's Trousers",
                        static='99,0:-1:110000,70000105:', shop=True, conditional=True),
        DS3LocationData("FS: Xanthous Overcoat - Xanthous Ashes", "Xanthous Overcoat", shop=True,
                        conditional=True),
        DS3LocationData("FS: Xanthous Gloves - Xanthous Ashes", "Xanthous Gloves", shop=True,
                        conditional=True),
        DS3LocationData("FS: Xanthous Trousers - Xanthous Ashes", "Xanthous Trousers", shop=True,
                        conditional=True),
        DS3LocationData("FS: Ember - Dragon Chaser's Ashes", "Ember",
                        static='99,0:-1:110000,70000108:', shop=True, conditional=True),
        DS3LocationData("FS: Washing Pole - Easterner's Ashes", "Washing Pole", shop=True,
                        conditional=True),
        DS3LocationData("FS: Eastern Helm - Easterner's Ashes", "Eastern Helm", shop=True,
                        conditional=True),
        DS3LocationData("FS: Eastern Armor - Easterner's Ashes", "Eastern Armor", shop=True,
                        conditional=True),
        DS3LocationData("FS: Eastern Gauntlets - Easterner's Ashes", "Eastern Gauntlets",
                        shop=True, conditional=True),
        DS3LocationData("FS: Eastern Leggings - Easterner's Ashes", "Eastern Leggings", shop=True,
                        conditional=True),
        DS3LocationData("FS: Wood Grain Ring - Easterner's Ashes", "Wood Grain Ring", shop=True,
                        conditional=True),
        DS3LocationData("FS: Millwood Knight Helm - Captain's Ashes", "Millwood Knight Helm",
                        dlc=True, shop=True, conditional=True),
        DS3LocationData("FS: Millwood Knight Armor - Captain's Ashes", "Millwood Knight Armor",
                        dlc=True, shop=True, conditional=True),
        DS3LocationData("FS: Millwood Knight Gauntlets - Captain's Ashes",
                        "Millwood Knight Gauntlets", dlc=True, shop=True, conditional=True),
        DS3LocationData("FS: Millwood Knight Leggings - Captain's Ashes",
                        "Millwood Knight Leggings", dlc=True, shop=True, conditional=True),
        DS3LocationData("FS: Refined Gem - Captain's Ashes", "Refined Gem", dlc=True, shop=True,
                        conditional=True),

        # Ludleth Shop
        DS3LocationData("FS: Vordt's Great Hammer - Ludleth for Vordt", "Vordt's Great Hammer",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Pontiff's Left Eye - Ludleth for Vordt", "Pontiff's Left Eye",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Bountiful Sunlight - Ludleth for Rosaria", "Bountiful Sunlight",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Darkmoon Longbow - Ludleth for Aldrich", "Darkmoon Longbow",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Lifehunt Scythe - Ludleth for Aldrich", "Lifehunt Scythe",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Hollowslayer Greatsword - Ludleth for Greatwood",
                        "Hollowslayer Greatsword", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Arstor's Spear - Ludleth for Greatwood", "Arstor's Spear",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Crystal Sage's Rapier - Ludleth for Sage", "Crystal Sage's Rapier",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Crystal Hail - Ludleth for Sage", "Crystal Hail", missable=True,
                        boss=True, shop=True),
        DS3LocationData("FS: Cleric's Candlestick - Ludleth for Deacons", "Cleric's Candlestick",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Deep Soul - Ludleth for Deacons", "Deep Soul", missable=True,
                        boss=True, shop=True),
        DS3LocationData("FS: Havel's Ring - Ludleth for Stray Demon", "Havel's Ring",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Boulder Heave - Ludleth for Stray Demon", "Boulder Heave",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Farron Greatsword - Ludleth for Abyss Watchers", "Farron Greatsword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Wolf Knight's Greatsword - Ludleth for Abyss Watchers",
                        "Wolf Knight's Greatsword", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Wolnir's Holy Sword - Ludleth for Wolnir", "Wolnir's Holy Sword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Black Serpent - Ludleth for Wolnir", "Black Serpent", missable=True,
                        boss=True, shop=True),
        DS3LocationData("FS: Demon's Greataxe - Ludleth for Fire Demon", "Demon's Greataxe",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Demon's Fist - Ludleth for Fire Demon", "Demon's Fist",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Old King's Great Hammer - Ludleth for Old Demon King",
                        "Old King's Great Hammer", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Chaos Bed Vestiges - Ludleth for Old Demon King", "Chaos Bed Vestiges",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Greatsword of Judgment - Ludleth for Pontiff",
                        "Greatsword of Judgment", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Profaned Greatsword - Ludleth for Pontiff", "Profaned Greatsword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Yhorm's Great Machete - Ludleth for Yhorm", "Yhorm's Great Machete",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Yhorm's Greatshield - Ludleth for Yhorm", "Yhorm's Greatshield",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Dancer's Enchanted Swords - Ludleth for Dancer",
                        "Dancer's Enchanted Swords", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Soothing Sunlight - Ludleth for Dancer", "Soothing Sunlight",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Dragonslayer Greataxe - Ludleth for Dragonslayer",
                        "Dragonslayer Greataxe", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Dragonslayer Greatshield - Ludleth for Dragonslayer",
                        "Dragonslayer Greatshield", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Moonlight Greatsword - Ludleth for Oceiros", "Moonlight Greatsword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: White Dragon Breath - Ludleth for Oceiros", "White Dragon Breath",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Lorian's Greatsword - Ludleth for Princes", "Lorian's Greatsword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Lothric's Holy Sword - Ludleth for Princes", "Lothric's Holy Sword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Gundyr's Halberd - Ludleth for Champion", "Gundyr's Halberd",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Prisoner's Chain - Ludleth for Champion", "Prisoner's Chain",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Storm Curved Sword - Ludleth for Nameless", "Storm Curved Sword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Dragonslayer Swordspear - Ludleth for Nameless",
                        "Dragonslayer Swordspear", missable=True, boss=True, shop=True),
        DS3LocationData("FS: Lightning Storm - Ludleth for Nameless", "Lightning Storm",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Firelink Greatsword - Ludleth for Cinder", "Firelink Greatsword",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Sunlight Spear - Ludleth for Cinder", "Sunlight Spear",
                        missable=True, boss=True, shop=True),
        DS3LocationData("FS: Friede's Great Scythe - Ludleth for Friede", "Friede's Great Scythe",
                        missable=True, dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Rose of Ariandel - Ludleth for Friede", "Rose of Ariandel",
                        missable=True, dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Demon's Scar - Ludleth for Demon Prince", "Demon's Scar",
                        missable=True, dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Seething Chaos - Ludleth for Demon Prince", "Seething Chaos",
                        missable=True, dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Frayed Blade - Ludleth for Midir", "Frayed Blade", missable=True,
                        dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Old Moonlight - Ludleth for Midir", "Old Moonlight", missable=True,
                        dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Gael's Greatsword - Ludleth for Gael", "Gael's Greatsword",
                        missable=True, dlc=True, boss=True, shop=True),
        DS3LocationData("FS: Repeating Crossbow - Ludleth for Gael", "Repeating Crossbow",
                        missable=True, dlc=True, boss=True, shop=True),
    ],
    "Firelink Shrine Bell Tower": [
        # Guarded by Tower Key
        DS3LocationData("FSBT: Homeward Bone - roof", "Homeward Bone x3"),
        DS3LocationData("FSBT: Estus Ring - tower base", "Estus Ring"),
        DS3LocationData("FSBT: Estus Shard - rafters", "Estus Shard"),
        DS3LocationData("FSBT: Fire Keeper Soul - tower top", "Fire Keeper Soul"),
        DS3LocationData("FSBT: Fire Keeper Robe - partway down tower", "Fire Keeper Robe"),
        DS3LocationData("FSBT: Fire Keeper Gloves - partway down tower", "Fire Keeper Gloves"),
        DS3LocationData("FSBT: Fire Keeper Skirt - partway down tower", "Fire Keeper Skirt"),
        DS3LocationData("FSBT: Covetous Silver Serpent Ring - illusory wall past rafters",
                        "Covetous Silver Serpent Ring", hidden=True),
        DS3LocationData("FSBT: Twinkling Titanite - lizard behind Firelink",
                        "Twinkling Titanite", lizard=True),

        # Mark all crow trades as missable since no one wants to have to try trading everything just
        # in case it gives a progression item.
        DS3LocationData("FSBT: Iron Bracelets - crow for Homeward Bone", "Iron Bracelets",
                        missable=True),
        DS3LocationData("FSBT: Ring of Sacrifice - crow for Loretta's Bone", "Ring of Sacrifice",
                        missable=True),
        DS3LocationData("FSBT: Porcine Shield - crow for Undead Bone Shard", "Porcine Shield",
                        missable=True),
        DS3LocationData("FSBT: Lucatiel's Mask - crow for Vertebra Shackle", "Lucatiel's Mask",
                        missable=True),
        DS3LocationData("FSBT: Very good! Carving - crow for Divine Blessing",
                        "Very good! Carving", missable=True),
        DS3LocationData("FSBT: Thank you Carving - crow for Hidden Blessing", "Thank you Carving",
                        missable=True),
        DS3LocationData("FSBT: I'm sorry Carving - crow for Shriving Stone", "I'm sorry Carving",
                        missable=True),
        DS3LocationData("FSBT: Sunlight Shield - crow for Mendicant's Staff", "Sunlight Shield",
                        missable=True),
        DS3LocationData("FSBT: Hollow Gem - crow for Eleonora", "Hollow Gem",
                        missable=True),
        DS3LocationData("FSBT: Titanite Scale - crow for Blacksmith Hammer", "Titanite Scale x3",
                        static='99,0:50004330::', missable=True),
        DS3LocationData("FSBT: Help me! Carving - crow for any sacred chime", "Help me! Carving",
                        missable=True),
        DS3LocationData("FSBT: Titanite Slab - crow for Coiled Sword Fragment", "Titanite Slab",
                        missable=True),
        DS3LocationData("FSBT: Hello Carving - crow for Alluring Skull", "Hello Carving",
                        missable=True),
        DS3LocationData("FSBT: Armor of the Sun - crow for Siegbräu", "Armor of the Sun",
                        missable=True),
        DS3LocationData("FSBT: Large Titanite Shard - crow for Firebomb", "Large Titanite Shard",
                        missable=True),
        DS3LocationData("FSBT: Titanite Chunk - crow for Black Firebomb", "Titanite Chunk",
                        missable=True),
        DS3LocationData("FSBT: Iron Helm - crow for Lightning Urn", "Iron Helm", missable=True),
        DS3LocationData("FSBT: Twinkling Titanite - crow for Prism Stone", "Twinkling Titanite",
                        missable=True),
        DS3LocationData("FSBT: Iron Leggings - crow for Seed of a Giant Tree", "Iron Leggings",
                        missable=True),
        DS3LocationData("FSBT: Lightning Gem - crow for Xanthous Crown", "Lightning Gem",
                        missable=True),
        DS3LocationData("FSBT: Twinkling Titanite - crow for Large Leather Shield",
                        "Twinkling Titanite", missable=True),
        DS3LocationData("FSBT: Blessed Gem - crow for Moaning Shield", "Blessed Gem",
                        missable=True),
    ],
    "High Wall of Lothric": [
        DS3LocationData("HWL: Soul of Boreal Valley Vordt", "Soul of Boreal Valley Vordt",
                        prominent=True, boss=True),
        DS3LocationData("HWL: Soul of the Dancer", "Soul of the Dancer", prominent=True,
                        boss=True),
        DS3LocationData("HWL: Basin of Vows - Emma", "Basin of Vows", prominent=True,
                        progression=True, conditional=True),
        DS3LocationData("HWL: Small Lothric Banner - Emma", "Small Lothric Banner",
                        prominent=True, progression=True),
        DS3LocationData("HWL: Green Blossom - fort walkway, hall behind wheel", "Green Blossom x2",
                        hidden=True),
        DS3LocationData("HWL: Gold Pine Resin - corpse tower, drop", "Gold Pine Resin x2",
                        hidden=True),
        DS3LocationData("HWL: Large Soul of a Deserted Corpse - flame plaza",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - by wall tower door",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Standard Arrow - back tower", "Standard Arrow x12"),
        DS3LocationData("HWL: Longbow - back tower", "Longbow"),
        DS3LocationData("HWL: Firebomb - wall tower, beam", "Firebomb x3"),
        DS3LocationData("HWL: Throwing Knife - wall tower, path to Greirat", "Throwing Knife x8"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - corpse tower, bottom floor",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Club - flame plaza", "Club"),
        DS3LocationData("HWL: Claymore - flame plaza", "Claymore"),
        DS3LocationData("HWL: Ember - flame plaza", "Ember"),
        DS3LocationData("HWL: Firebomb - corpse tower, under table", "Firebomb x2"),
        DS3LocationData("HWL: Titanite Shard - wall tower, corner by bonfire", "Titanite Shard",
                        hidden=True),
        DS3LocationData("HWL: Undead Hunter Charm - fort, room off entry, in pot",
                        "Undead Hunter Charm x2", hidden=True),
        DS3LocationData("HWL: Firebomb - top of ladder to fountain", "Firebomb x3"),
        DS3LocationData("HWL: Cell Key - fort ground, down stairs", "Cell Key"),
        DS3LocationData("HWL: Ember - fountain #1", "Ember"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - fort entry, corner",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Lucerne - promenade, side path", "Lucerne"),
        DS3LocationData("HWL: Mail Breaker - wall tower, path to Greirat", "Mail Breaker"),
        DS3LocationData("HWL: Titanite Shard - fort ground behind crates", "Titanite Shard",
                        hidden=True),
        DS3LocationData("HWL: Rapier - fountain, corner", "Rapier"),
        DS3LocationData("HWL: Titanite Shard - fort, room off entry", "Titanite Shard"),
        DS3LocationData("HWL: Large Soul of a Deserted Corpse - fort roof",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Black Firebomb - small roof over fountain", "Black Firebomb x3"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - path to corpse tower",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Ember - fountain #2", "Ember"),
        DS3LocationData("HWL: Large Soul of a Deserted Corpse - platform by fountain",
                        "Large Soul of a Deserted Corpse", hidden=True),  # Easily missed turnoff
        DS3LocationData("HWL: Binoculars - corpse tower, upper platform", "Binoculars"),
        DS3LocationData("HWL: Ring of Sacrifice - awning by fountain",
                        "Ring of Sacrifice", hidden=True),  # Easily missed turnoff
        DS3LocationData("HWL: Throwing Knife - shortcut, lift top", "Throwing Knife x6"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - path to back tower, by lift door",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Green Blossom - shortcut, lower courtyard", "Green Blossom x3"),
        DS3LocationData("HWL: Broadsword - fort, room off walkway", "Broadsword"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - fountain, path to promenade",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Firebomb - fort roof", "Firebomb x3"),
        DS3LocationData("HWL: Soul of a Deserted Corpse - wall tower, right of exit",
                        "Soul of a Deserted Corpse"),
        DS3LocationData("HWL: Estus Shard - fort ground, on anvil", "Estus Shard"),
        DS3LocationData("HWL: Fleshbite Ring+1 - fort roof, jump to other roof",
                        "Fleshbite Ring+1", ngp=True, hidden=True),  # Hidden jump
        DS3LocationData("HWL: Ring of the Evil Eye+2 - fort ground, far wall",
                        "Ring of the Evil Eye+2", ngp=True, hidden=True),  # In barrels
        DS3LocationData("HWL: Silver Eagle Kite Shield - fort mezzanine",
                        "Silver Eagle Kite Shield"),
        DS3LocationData("HWL: Astora Straight Sword - fort walkway, drop down",
                        "Astora Straight Sword", hidden=True),  # Hidden fall
        DS3LocationData("HWL: Battle Axe - flame tower, mimic", "Battle Axe",
                        static='01,0:53000960::', mimic=True),

        # Only dropped after transformation
        DS3LocationData("HWL: Ember - fort roof, transforming hollow", "Ember", hidden=True),
        DS3LocationData("HWL: Titanite Shard - fort roof, transforming hollow", "Titanite Shard",
                        hidden=True),
        DS3LocationData("HWL: Ember - back tower, transforming hollow", "Ember", hidden=True),
        DS3LocationData("HWL: Titanite Shard - back tower, transforming hollow", "Titanite Shard",
                        hidden=True),

        DS3LocationData("HWL: Refined Gem - promenade miniboss", "Refined Gem", miniboss=True),
        DS3LocationData("HWL: Way of Blue - Emma", "Way of Blue"),
        # Categorize this as an NPC item so that it doesn't get randomized if the Lift Chamber Key
        # isn't randomized, since in that case it's missable.
        DS3LocationData("HWL: Red Eye Orb - wall tower, miniboss", "Red Eye Orb",
                        conditional=True, miniboss=True, npc=True),
        DS3LocationData("HWL: Raw Gem - fort roof, lizard", "Raw Gem", lizard=True),
    ],
    "Undead Settlement": [
        DS3LocationData("US: Soul of the Rotted Greatwood", "Soul of the Rotted Greatwood",
                        prominent=True, boss=True),
        DS3LocationData("US: Transposing Kiln - boss drop", "Transposing Kiln", boss=True),
        # Missable because it's unavailable if you start as a Pyromancer
        DS3LocationData("US: Pyromancy Flame - Cornyx", "Pyromancy Flame", missable=True,
                        npc=True),
        DS3LocationData("US: Old Sage's Blindfold - kill Cornyx", "Old Sage's Blindfold",
                        npc=True),
        DS3LocationData("US: Cornyx's Garb - kill Cornyx", "Cornyx's Garb",
                        static='02,0:50006141::', npc=True),
        DS3LocationData("US: Cornyx's Wrap - kill Cornyx", "Cornyx's Wrap",
                        static='02,0:50006141::', npc=True),
        DS3LocationData("US: Cornyx's Skirt - kill Cornyx", "Cornyx's Skirt",
                        static='02,0:50006141::', npc=True),
        DS3LocationData("US: Tower Key - kill Irina", "Tower Key", missable=True, npc=True),
        DS3LocationData("US: Flynn's Ring - tower village, rooftop", "Flynn's Ring"),
        DS3LocationData("US: Undead Bone Shard - by white tree", "Undead Bone Shard"),
        DS3LocationData("US: Alluring Skull - foot, behind carriage", "Alluring Skull x2"),
        DS3LocationData("US: Mortician's Ashes - graveyard by white tree", "Mortician's Ashes",
                        progression=True),
        DS3LocationData("US: Homeward Bone - tower village, jump from roof", "Homeward Bone x2",
                        static='02,0:53100040::', hidden=True),  # Hidden fall
        DS3LocationData("US: Caduceus Round Shield - right after stable exit",
                        "Caduceus Round Shield"),
        DS3LocationData("US: Ember - tower basement, miniboss", "Ember"),
        DS3LocationData("US: Soul of an Unknown Traveler - chasm crypt",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("US: Repair Powder - first building, balcony", "Repair Powder x2"),
        DS3LocationData("US: Homeward Bone - stable roof", "Homeward Bone x2",
                        static='02,0:53100090::'),
        DS3LocationData("US: Titanite Shard - back alley, side path", "Titanite Shard"),
        DS3LocationData("US: Wargod Wooden Shield - Pit of Hollows", "Wargod Wooden Shield"),
        DS3LocationData("US: Large Soul of a Deserted Corpse - on the way to tower, by well",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("US: Ember - bridge on the way to tower", "Ember"),
        DS3LocationData("US: Large Soul of a Deserted Corpse - stable",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("US: Titanite Shard - porch after burning tree", "Titanite Shard"),
        DS3LocationData("US: Alluring Skull - tower village building, upstairs",
                        "Alluring Skull x2"),
        DS3LocationData("US: Charcoal Pine Bundle - first building, middle floor",
                        "Charcoal Pine Bundle x2"),
        DS3LocationData("US: Blue Wooden Shield - graveyard by white tree", "Blue Wooden Shield"),
        DS3LocationData("US: Cleric Hat - graveyard by white tree", "Cleric Hat"),
        DS3LocationData("US: Cleric Blue Robe - graveyard by white tree", "Cleric Blue Robe"),
        DS3LocationData("US: Cleric Gloves - graveyard by white tree", "Cleric Gloves"),
        DS3LocationData("US: Cleric Trousers - graveyard by white tree", "Cleric Trousers"),
        DS3LocationData("US: Soul of an Unknown Traveler - portcullis by burning tree",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("US: Charcoal Pine Resin - hanging corpse room", "Charcoal Pine Resin x2"),
        DS3LocationData("US: Loincloth - by Velka statue", "Loincloth"),
        DS3LocationData("US: Bloodbite Ring - miniboss in sewer", "Bloodbite Ring",
                        miniboss=True),  # Giant Rat drop
        DS3LocationData("US: Charcoal Pine Bundle - first building, bottom floor",
                        "Charcoal Pine Bundle x2"),
        DS3LocationData("US: Soul of an Unknown Traveler - back alley, past crates",
                        "Soul of an Unknown Traveler", hidden=True),
        DS3LocationData("US: Titanite Shard - back alley, up ladder", "Titanite Shard"),
        DS3LocationData("US: Red Hilted Halberd - chasm crypt", "Red Hilted Halberd"),
        DS3LocationData("US: Rusted Coin - awning above Dilapidated Bridge", "Rusted Coin x2"),
        DS3LocationData("US: Caestus - sewer", "Caestus"),
        DS3LocationData("US: Saint's Talisman - chasm, by ladder", "Saint's Talisman"),
        DS3LocationData("US: Alluring Skull - on the way to tower, behind building",
                        "Alluring Skull x3"),
        DS3LocationData("US: Large Club - tower village, by miniboss", "Large Club"),
        DS3LocationData("US: Titanite Shard - chasm #1", "Titanite Shard"),
        DS3LocationData("US: Titanite Shard - chasm #2", "Titanite Shard"),
        DS3LocationData("US: Fading Soul - outside stable", "Fading Soul"),
        DS3LocationData("US: Titanite Shard - lower path to Cliff Underside", "Titanite Shard",
                        hidden=True),  # hidden fall
        DS3LocationData("US: Hand Axe - by Cornyx", "Hand Axe"),
        DS3LocationData("US: Soul of an Unknown Traveler - pillory past stable",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("US: Ember - by stairs to boss", "Ember"),
        DS3LocationData("US: Mirrah Vest - tower village, jump from roof", "Mirrah Vest",
                        hidden=True),  # Hidden fall
        DS3LocationData("US: Mirrah Gloves - tower village, jump from roof", "Mirrah Gloves",
                        hidden=True),  # Hidden fall
        DS3LocationData("US: Mirrah Trousers - tower village, jump from roof", "Mirrah Trousers",
                        hidden=True),  # Hidden fall
        DS3LocationData("US: Plank Shield - outside stable, by NPC", "Plank Shield"),
        DS3LocationData("US: Red Bug Pellet - tower village building, basement",
                        "Red Bug Pellet x2"),
        DS3LocationData("US: Chloranthy Ring - tower village, jump from roof", "Chloranthy Ring",
                        hidden=True),  # Hidden fall
        DS3LocationData("US: Fire Clutch Ring - wooden walkway past stable", "Fire Clutch Ring"),
        DS3LocationData("US: Estus Shard - under burning tree", "Estus Shard"),
        DS3LocationData("US: Firebomb - stable roof", "Firebomb x6"),
        # In enemy rando, the enemy may not burst through the wall and make this room obvious
        DS3LocationData("US: Whip - back alley, behind wooden wall", "Whip", hidden=True),
        DS3LocationData("US: Great Scythe - building by white tree, balcony", "Great Scythe"),
        DS3LocationData("US: Homeward Bone - foot, drop overlook", "Homeward Bone",
                        static='02,0:53100950::'),
        DS3LocationData("US: Large Soul of a Deserted Corpse - around corner by Cliff Underside",
                        "Large Soul of a Deserted Corpse", hidden=True),  # Hidden corner
        DS3LocationData("US: Ember - behind burning tree", "Ember"),
        DS3LocationData("US: Large Soul of a Deserted Corpse - across from Foot of the High Wall",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("US: Fading Soul - by white tree", "Fading Soul"),
        DS3LocationData("US: Young White Branch - by white tree #1", "Young White Branch"),
        DS3LocationData("US: Ember - by white tree", "Ember"),
        DS3LocationData("US: Large Soul of a Deserted Corpse - by white tree",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("US: Young White Branch - by white tree #2", "Young White Branch"),
        DS3LocationData("US: Reinforced Club - by white tree", "Reinforced Club"),
        DS3LocationData("US: Soul of a Nameless Soldier - top of tower",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("US: Loretta's Bone - first building, hanging corpse on balcony",
                        "Loretta's Bone"),
        DS3LocationData("US: Northern Helm - tower village, hanging corpse", "Northern Helm"),
        DS3LocationData("US: Northern Armor - tower village, hanging corpse", "Northern Armor"),
        DS3LocationData("US: Northern Gloves - tower village, hanging corpse", "Northern Gloves"),
        DS3LocationData("US: Northern Trousers - tower village, hanging corpse",
                        "Northern Trousers"),
        DS3LocationData("US: Partizan - hanging corpse above Cliff Underside", "Partizan",
                        missable=True),  # requires projectile
        DS3LocationData("US: Flame Stoneplate Ring - hanging corpse by Mound-Maker transport",
                        "Flame Stoneplate Ring"),
        DS3LocationData("US: Red and White Round Shield - chasm, hanging corpse",
                        "Red and White Round Shield", static="02,0:53100740::",
                        missable=True),  # requires projectile
        DS3LocationData("US: Small Leather Shield - first building, hanging corpse by entrance",
                        "Small Leather Shield"),
        DS3LocationData("US: Pale Tongue - tower village, hanging corpse", "Pale Tongue"),
        DS3LocationData("US: Large Soul of a Deserted Corpse - hanging corpse room, over stairs",
                        "Large Soul of a Deserted Corpse"),
        DS3LocationData("US: Kukri - hanging corpse above burning tree", "Kukri x9",
                        missable=True),  # requires projectile
        DS3LocationData("US: Life Ring+1 - tower on the way to village", "Life Ring+1", ngp=True),
        DS3LocationData("US: Poisonbite Ring+1 - graveyard by white tree, near well",
                        "Poisonbite Ring+1", ngp=True),
        DS3LocationData("US: Covetous Silver Serpent Ring+2 - tower village, drop down from roof",
                        "Covetous Silver Serpent Ring+2", ngp=True, hidden=True),  # Hidden fall
        DS3LocationData("US: Human Pine Resin - tower village building, chest upstairs",
                        "Human Pine Resin x4"),
        DS3LocationData("US: Homeward Bone - tower village, right at start", "Homeward Bone",
                        static='02,0:53100540::'),
        DS3LocationData("US: Irithyll Straight Sword - miniboss drop, by Road of Sacrifices",
                        "Irithyll Straight Sword", miniboss=True),
        DS3LocationData("US: Fire Gem - tower village, miniboss drop", "Fire Gem", miniboss=True),
        DS3LocationData("US: Warrior of Sunlight - hanging corpse room, drop through hole",
                        "Warrior of Sunlight", hidden=True),  # hidden fall
        DS3LocationData("US: Mound-makers - Hodrick", "Mound-makers", missable=True),
        DS3LocationData("US: Sharp Gem - lizard by Dilapidated Bridge", "Sharp Gem", lizard=True),
        DS3LocationData("US: Heavy Gem - chasm, lizard", "Heavy Gem", lizard=True),
        DS3LocationData("US: Siegbräu - Siegward", "Siegbräu", missable=True, npc=True),
        DS3LocationData("US: Heavy Gem - Hawkwood", "Heavy Gem", static='00,0:50006070::',
                        missable=True, npc=True),  # Hawkwood (quest, after Greatwood or Sage)
        DS3LocationData("US -> RS", None),

        # Yoel/Yuria of Londor
        DS3LocationData("FS: Soul Arrow - Yoel/Yuria shop", "Soul Arrow",
                        static='99,0:-1:50000,110000,70000116:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Heavy Soul Arrow - Yoel/Yuria shop", "Heavy Soul Arrow",
                        static='99,0:-1:50000,110000,70000116:',
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Magic Weapon - Yoel/Yuria shop", "Magic Weapon",
                        static='99,0:-1:50000,110000,70000116:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Magic Shield - Yoel/Yuria shop", "Magic Shield",
                        static='99,0:-1:50000,110000,70000116:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Soul Greatsword - Yoel/Yuria shop", "Soul Greatsword",
                        static='99,0:-1:50000,110000,70000450,70000475:', missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Dark Hand - Yuria shop", "Dark Hand", missable=True, npc=True),
        DS3LocationData("FS: Untrue White Ring - Yuria shop", "Untrue White Ring", missable=True,
                        npc=True),
        DS3LocationData("FS: Untrue Dark Ring - Yuria shop", "Untrue Dark Ring", missable=True,
                        npc=True),
        DS3LocationData("FS: Londor Braille Divine Tome - Yuria shop", "Londor Braille Divine Tome",
                        static='99,0:-1:40000,110000,70000116:', missable=True, npc=True),
        DS3LocationData("FS: Darkdrift - kill Yuria", "Darkdrift", missable=True, drop=True,
                        npc=True),  # kill her or kill Soul of Cinder

        # Cornyx of the Great Swamp
        # These aren't missable because the Shrine Handmaid will carry them if you kill Cornyx.
        DS3LocationData("FS: Fireball - Cornyx", "Fireball", npc=True, shop=True),
        DS3LocationData("FS: Fire Surge - Cornyx", "Fire Surge", npc=True, shop=True),
        DS3LocationData("FS: Great Combustion - Cornyx", "Great Combustion", npc=True,
                        shop=True),
        DS3LocationData("FS: Flash Sweat - Cornyx", "Flash Sweat", npc=True, shop=True),
        # These are missable if you kill Cornyx before giving him the right tomes.
        DS3LocationData("FS: Poison Mist - Cornyx for Great Swamp Tome", "Poison Mist",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Fire Orb - Cornyx for Great Swamp Tome", "Fire Orb", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Profuse Sweat - Cornyx for Great Swamp Tome", "Profuse Sweat",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Bursting Fireball - Cornyx for Great Swamp Tome", "Bursting Fireball",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Acid Surge - Cornyx for Carthus Tome", "Acid Surge", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Carthus Flame Arc - Cornyx for Carthus Tome", "Carthus Flame Arc",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Carthus Beacon - Cornyx for Carthus Tome", "Carthus Beacon",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Great Chaos Fire Orb - Cornyx for Izalith Tome",
                        "Great Chaos Fire Orb", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Chaos Storm - Cornyx for Izalith Tome", "Chaos Storm", missable=True,
                        npc=True, shop=True),

        # Irina of Carim
        # These aren't in their own location because you don't actually need the Grave Key to access
        # Irena—you can just fall down the cliff near Eygon.
        DS3LocationData("FS: Saint's Ring - Irina", "Saint's Ring", npc=True, shop=True),
        DS3LocationData("FS: Heal - Irina", "Heal", npc=True, shop=True),
        DS3LocationData("FS: Replenishment - Irina", "Replenishment", npc=True, shop=True),
        DS3LocationData("FS: Caressing Tears - Irina", "Caressing Tears", npc=True, shop=True),
        DS3LocationData("FS: Homeward - Irina", "Homeward", npc=True, shop=True),
        DS3LocationData("FS: Med Heal - Irina for Tome of Carim", "Med Heal", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Tears of Denial - Irina for Tome of Carim", "Tears of Denial",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Force - Irina for Tome of Carim", "Force", missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Bountiful Light - Irina for Tome of Lothric", "Bountiful Light",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Magic Barrier - Irina for Tome of Lothric", "Magic Barrier",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Blessed Weapon - Irina for Tome of Lothric", "Blessed Weapon",
                        missable=True, npc=True, shop=True),
    ],
    "Road of Sacrifices": [
        DS3LocationData("RS: Soul of a Crystal Sage", "Soul of a Crystal Sage", prominent=True,
                        boss=True),
        DS3LocationData("RS: Exile Greatsword - NPC drop by Farron Keep", "Exile Greatsword",
                        hostile_npc=True),  # Exile Knight #2 drop
        DS3LocationData("RS: Great Club - NPC drop by Farron Keep", "Great Club",
                        hostile_npc=True),  # Exile Knight #1 drop
        DS3LocationData("RS: Heysel Pick - Heysel drop", "Heysel Pick", missable=True,
                        hostile_npc=True),
        DS3LocationData("RS: Xanthous Crown - Heysel drop", "Xanthous Crown", missable=True,
                        hostile_npc=True),
        DS3LocationData("RS: Butcher Knife - NPC drop beneath road", "Butcher Knife",
                        hostile_npc=True),  # Madwoman
        DS3LocationData("RS: Titanite Shard - water by Halfway Fortress", "Titanite Shard"),
        DS3LocationData("RS: Titanite Shard - woods, left of path from Halfway Fortress",
                        "Titanite Shard"),
        DS3LocationData("RS: Green Blossom - by deep water", "Green Blossom x4"),
        DS3LocationData("RS: Estus Shard - left of fire behind stronghold left room",
                        "Estus Shard"),
        DS3LocationData("RS: Ring of Sacrifice - stronghold, drop from right room balcony",
                        "Ring of Sacrifice", hidden=True),  # hidden fall
        DS3LocationData("RS: Soul of an Unknown Traveler - drop along wall from Halfway Fortress",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("RS: Fallen Knight Helm - water's edge by Farron Keep",
                        "Fallen Knight Helm"),
        DS3LocationData("RS: Fallen Knight Armor - water's edge by Farron Keep",
                        "Fallen Knight Armor"),
        DS3LocationData("RS: Fallen Knight Gauntlets - water's edge by Farron Keep",
                        "Fallen Knight Gauntlets"),
        DS3LocationData("RS: Fallen Knight Trousers - water's edge by Farron Keep",
                        "Fallen Knight Trousers"),
        DS3LocationData("RS: Heretic's Staff - stronghold left room", "Heretic's Staff"),
        DS3LocationData("RS: Large Soul of an Unknown Traveler - left of stairs to Farron Keep",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("RS: Conjurator Hood - deep water", "Conjurator Hood"),
        DS3LocationData("RS: Conjurator Robe - deep water", "Conjurator Robe"),
        DS3LocationData("RS: Conjurator Manchettes - deep water", "Conjurator Manchettes"),
        DS3LocationData("RS: Conjurator Boots - deep water", "Conjurator Boots"),
        DS3LocationData("RS: Soul of an Unknown Traveler - right of door to stronghold left",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("RS: Green Blossom - water beneath stronghold", "Green Blossom x2"),
        DS3LocationData("RS: Great Swamp Pyromancy Tome - deep water",
                        "Great Swamp Pyromancy Tome"),
        DS3LocationData("RS: Homeward Bone - balcony by Farron Keep", "Homeward Bone x2"),
        DS3LocationData("RS: Titanite Shard - woods, surrounded by enemies", "Titanite Shard"),
        DS3LocationData("RS: Twin Dragon Greatshield - woods by Crucifixion Woods bonfire",
                        "Twin Dragon Greatshield", missable=True), # After Eclipse
        DS3LocationData("RS: Sorcerer Hood - water beneath stronghold", "Sorcerer Hood",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Sorcerer Robe - water beneath stronghold", "Sorcerer Robe",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Sorcerer Gloves - water beneath stronghold", "Sorcerer Gloves",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Sorcerer Trousers - water beneath stronghold", "Sorcerer Trousers",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Sage Ring - water beneath stronghold", "Sage Ring",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Grass Crest Shield - water by Crucifixion Woods bonfire",
                        "Grass Crest Shield"),
        DS3LocationData("RS: Ember - right of fire behind stronghold left room", "Ember"),
        DS3LocationData("RS: Blue Bug Pellet - broken stairs by Orbeck", "Blue Bug Pellet x2"),
        DS3LocationData("RS: Soul of an Unknown Traveler - road, by wagon",
                        "Soul of an Unknown Traveler"),
        DS3LocationData("RS: Shriving Stone - road, by start", "Shriving Stone"),
        DS3LocationData("RS: Titanite Shard - road, on bridge after you go under",
                        "Titanite Shard"),
        DS3LocationData("RS: Brigand Twindaggers - beneath road", "Brigand Twindaggers"),
        DS3LocationData("RS: Braille Divine Tome of Carim - drop from bridge to Halfway Fortress",
                        "Braille Divine Tome of Carim", hidden=True),  # Hidden fall
        DS3LocationData("RS: Ember - right of Halfway Fortress entrance", "Ember"),
        DS3LocationData("RS: Sellsword Twinblades - keep perimeter", "Sellsword Twinblades"),
        DS3LocationData("RS: Golden Falcon Shield - path from stronghold right room to Farron Keep",
                        "Golden Falcon Shield"),
        DS3LocationData("RS: Brigand Axe - beneath road", "Brigand Axe"),
        DS3LocationData("RS: Brigand Hood - beneath road", "Brigand Hood"),
        DS3LocationData("RS: Brigand Armor - beneath road", "Brigand Armor"),
        DS3LocationData("RS: Brigand Gauntlets - beneath road", "Brigand Gauntlets"),
        DS3LocationData("RS: Brigand Trousers - beneath road", "Brigand Trousers"),
        DS3LocationData("RS: Morne's Ring - drop from bridge to Halfway Fortress", "Morne's Ring",
                        hidden=True),  # Hidden fall
        DS3LocationData("RS: Sellsword Helm - keep perimeter balcony", "Sellsword Helm"),
        DS3LocationData("RS: Sellsword Armor - keep perimeter balcony", "Sellsword Armor"),
        DS3LocationData("RS: Sellsword Gauntlet - keep perimeter balcony", "Sellsword Gauntlet"),
        DS3LocationData("RS: Sellsword Trousers - keep perimeter balcony", "Sellsword Trousers"),
        DS3LocationData("RS: Farron Coal - keep perimeter", "Farron Coal"),
        DS3LocationData("RS: Chloranthy Ring+2 - road, drop across from carriage",
                        "Chloranthy Ring+2", hidden=True, ngp=True),  # Hidden fall
        DS3LocationData("RS: Lingering Dragoncrest Ring+1 - water", "Lingering Dragoncrest Ring+1",
                        ngp=True),
        DS3LocationData("RS: Great Swamp Ring - miniboss drop, by Farron Keep",
                        "Great Swamp Ring", miniboss=True),  # Giant Crab drop
        DS3LocationData("RS: Blue Sentinels - Horace", "Blue Sentinels",
                        missable=True, npc=True),  # Horace quest
        DS3LocationData("RS: Crystal Gem - stronghold, lizard", "Crystal Gem", lizard=True),
        DS3LocationData("RS: Fading Soul - woods by Crucifixion Woods bonfire", "Fading Soul",
                        static='03,0:53300210::'),

        # Orbeck shop, all missable because he'll disappear if you don't talk to him for too long or
        # if you don't give him a scroll.
        DS3LocationData("FS: Farron Dart - Orbeck", "Farron Dart",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Soul Arrow - Orbeck", "Soul Arrow",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Great Soul Arrow - Orbeck", "Great Soul Arrow", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Heavy Soul Arrow - Orbeck", "Heavy Soul Arrow",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Great Heavy Soul Arrow - Orbeck", "Great Heavy Soul Arrow",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Magic Weapon - Orbeck", "Magic Weapon",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Magic Shield - Orbeck", "Magic Shield",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Spook - Orbeck", "Spook", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Aural Decoy - Orbeck", "Aural Decoy", missable=True, npc=True,
                        shop=True),
        DS3LocationData("FS: Soul Greatsword - Orbeck", "Soul Greatsword",
                        static='99,0:-1:110000,130100,70000111:', missable=True, npc=True),
        DS3LocationData("FS: Farron Flashsword - Orbeck", "Farron Flashsword", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Pestilent Mist - Orbeck for any scroll", "Pestilent Mist",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Great Farron Dart - Orbeck for Sage's Scroll", "Great Farron Dart",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Farron Hail - Orbeck for Sage's Scroll", "Farron Hail",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Homing Soulmass - Orbeck for Logan's Scroll", "Homing Soulmass",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Soul Spear - Orbeck for Logan's Scroll", "Soul Spear",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Homing Crystal Soulmass - Orbeck for Crystal Scroll",
                        "Homing Crystal Soulmass", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Crystal Soul Spear - Orbeck for Crystal Scroll", "Crystal Soul Spear",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Crystal Magic Weapon - Orbeck for Crystal Scroll",
                        "Crystal Magic Weapon", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Cast Light - Orbeck for Golden Scroll", "Cast Light", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Twisted Wall of Light - Orbeck for Golden Scroll",
                        "Twisted Wall of Light", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Hidden Weapon - Orbeck for Golden Scroll", "Hidden Weapon",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Hidden Body - Orbeck for Golden Scroll", "Hidden Body",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Repair - Orbeck for Golden Scroll", "Repair", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Clandestine Coat - shop with Orbeck's Ashes", "Clandestine Coat",
                        missable=True, npc=True,
                        shop=True),  # Shrine Handmaid with Orbeck's Ashes + reload
        DS3LocationData("FS: Young Dragon Ring - Orbeck for one scroll and buying three spells",
                        "Young Dragon Ring", missable=True, npc=True),
        DS3LocationData("FS: Slumbering Dragoncrest Ring - Orbeck for buying four specific spells",
                        "Slumbering Dragoncrest Ring", missable=True, npc=True),
        DS3LocationData("RS -> FK", None),

        # Shrine Handmaid after killing exiles
        DS3LocationData("FS: Exile Mask - shop after killing NPCs in RS", "Exile Mask",
                        hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Exile Armor - shop after killing NPCs in RS", "Exile Armor",
                        hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Exile Gauntlets - shop after killing NPCs in RS", "Exile Gauntlets",
                        hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Exile Leggings - shop after killing NPCs in RS", "Exile Leggings",
                        hostile_npc=True, shop=True, hidden=True),

        # Shrine Handmaid after killing Crystal Sage
        DS3LocationData("FS: Sage's Big Hat - shop after killing RS boss", "Sage's Big Hat",
                        boss=True, shop=True),

        # Yuria of Londor for Orbeck's Ashes
        DS3LocationData("FS: Morion Blade - Yuria for Orbeck's Ashes", "Morion Blade",
                        missable=True, npc=True),
    ],
    "Cathedral of the Deep": [
        DS3LocationData("CD: Herald Helm - path, by fire", "Herald Helm"),
        DS3LocationData("CD: Herald Armor - path, by fire", "Herald Armor"),
        DS3LocationData("CD: Herald Gloves - path, by fire", "Herald Gloves"),
        DS3LocationData("CD: Herald Trousers - path, by fire", "Herald Trousers"),
        DS3LocationData("CD: Twinkling Titanite - path, lizard #1", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("CD: Twinkling Titanite - path, lizard #2", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("CD: Small Doll - boss drop", "Small Doll", prominent=True,
                        progression=True, boss=True),
        DS3LocationData("CD: Soul of the Deacons of the Deep", "Soul of the Deacons of the Deep",
                        boss=True),
        DS3LocationData("CD: Black Eye Orb - Rosaria from Leonhard's quest", "Black Eye Orb",
                        missable=True, npc=True),
        DS3LocationData("CD: Winged Spear - kill Patches", "Winged Spear", drop=True,
                        missable=True),  # Patches (kill)
        DS3LocationData("CD: Spider Shield - NPC drop on path", "Spider Shield",
                        hostile_npc=True),  # Brigand
        DS3LocationData("CD: Notched Whip - Cleansing Chapel", "Notched Whip"),
        DS3LocationData("CD: Titanite Shard - Cleansing Chapel windowsill, by miniboss",
                        "Titanite Shard"),
        DS3LocationData("CD: Astora Greatsword - graveyard, left of entrance", "Astora Greatsword"),
        DS3LocationData("CD: Executioner's Greatsword - graveyard, far end",
                        "Executioner's Greatsword"),
        DS3LocationData("CD: Undead Bone Shard - gravestone by white tree", "Undead Bone Shard"),
        DS3LocationData("CD: Curse Ward Greatshield - by ladder from white tree to moat",
                        "Curse Ward Greatshield"),
        DS3LocationData("CD: Titanite Shard - moat, far end", "Titanite Shard"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - lower roofs, semicircle balcony",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CD: Paladin's Ashes - path, guarded by lower NPC", "Paladin's Ashes",
                        progression=True),
        DS3LocationData("CD: Arbalest - upper roofs, end of furthest buttress", "Arbalest"),
        DS3LocationData("CD: Ember - by back door", "Ember"),
        DS3LocationData("CD: Ember - side chapel upstairs, up ladder", "Ember"),
        DS3LocationData("CD: Poisonbite Ring - moat, hall past miniboss", "Poisonbite Ring"),
        DS3LocationData("CD: Drang Armor - main hall, east", "Drang Armor"),
        DS3LocationData("CD: Ember - edge of platform before boss", "Ember"),
        DS3LocationData("CD: Duel Charm - next to Patches in onion armor", "Duel Charm x3"),
        DS3LocationData("CD: Seek Guidance - side chapel upstairs", "Seek Guidance"),
        DS3LocationData("CD: Estus Shard - monument outside Cleansing Chapel", "Estus Shard"),
        DS3LocationData("CD: Maiden Hood - main hall south", "Maiden Hood"),
        DS3LocationData("CD: Maiden Robe - main hall south", "Maiden Robe"),
        DS3LocationData("CD: Maiden Gloves - main hall south", "Maiden Gloves"),
        DS3LocationData("CD: Maiden Skirt - main hall south", "Maiden Skirt"),
        DS3LocationData("CD: Pale Tongue - upper roofs, outdoors far end", "Pale Tongue"),
        DS3LocationData("CD: Fading Soul - graveyard, far end", "Fading Soul"),
        DS3LocationData("CD: Blessed Gem - upper roofs, rafters", "Blessed Gem"),
        DS3LocationData("CD: Red Bug Pellet - right of cathedral front doors", "Red Bug Pellet"),
        DS3LocationData("CD: Soul of a Nameless Soldier - main hall south",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("CD: Duel Charm - by first elevator", "Duel Charm"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - main hall south, side path",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CD: Ember - side chapel, miniboss room", "Ember"),
        DS3LocationData("CD: Repair Powder - by white tree", "Repair Powder x3"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - by white tree #1",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - by white tree #2",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CD: Undead Hunter Charm - lower roofs, up stairs between buttresses",
                        "Undead Hunter Charm x3"),
        DS3LocationData("CD: Red Bug Pellet - lower roofs, up stairs between buttresses",
                        "Red Bug Pellet x3"),
        DS3LocationData("CD: Titanite Shard - outside building by white tree", "Titanite Shard",
                        hidden=True),  # Easily missable side path
        DS3LocationData("CD: Titanite Shard - moat, up a slope", "Titanite Shard"),
        DS3LocationData("CD: Rusted Coin - left of cathedral front doors, behind crates",
                        "Rusted Coin x2", hidden=True),
        DS3LocationData("CD: Drang Hammers - main hall east", "Drang Hammers"),
        DS3LocationData("CD: Drang Shoes - main hall east", "Drang Shoes"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - main hall east",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CD: Pale Tongue - main hall east", "Pale Tongue"),
        DS3LocationData("CD: Drang Gauntlets - main hall east", "Drang Gauntlets"),
        DS3LocationData("CD: Soul of a Nameless Soldier - lower roofs, side room",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("CD: Exploding Bolt - ledge above main hall south", "Exploding Bolt x6"),
        DS3LocationData("CD: Lloyd's Sword Ring - ledge above main hall south",
                        "Lloyd's Sword Ring"),
        DS3LocationData("CD: Soul of a Nameless Soldier - ledge above main hall south",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("CD: Homeward Bone - outside main hall south door", "Homeward Bone x2"),
        DS3LocationData("CD: Deep Gem - down stairs by first elevator", "Deep Gem"),
        DS3LocationData("CD: Titanite Shard - path, side path by Cathedral of the Deep bonfire",
                        "Titanite Shard"),
        DS3LocationData("CD: Large Soul of an Unknown Traveler - path, against outer wall",
                        "Large Soul of an Unknown Traveler"),
        # Before the stairs leading down into the Deacons fight
        DS3LocationData("CD: Ring of the Evil Eye+1 - by stairs to boss", "Ring of the Evil Eye+1",
                        ngp=True),
        DS3LocationData("CD: Ring of Favor+2 - upper roofs, on buttress", "Ring of Favor+2",
                        hidden=True, ngp=True),  # Hidden fall
        DS3LocationData("CD: Crest Shield - path, drop down by Cathedral of the Deep bonfire",
                        "Crest Shield", hidden=True),  # Hidden fall
        DS3LocationData("CD: Young White Branch - by white tree #1", "Young White Branch"),
        DS3LocationData("CD: Young White Branch - by white tree #2", "Young White Branch"),
        DS3LocationData("CD: Saint-tree Bellvine - moat, by water", "Saint-tree Bellvine"),
        DS3LocationData("CD: Saint Bident - outside main hall south door", "Saint Bident"),
        # Archdeacon set is hidden because you have to return to a cleared area
        DS3LocationData("CD: Archdeacon White Crown - boss room after killing boss",
                        "Archdeacon White Crown", boss=True, hidden=True),
        DS3LocationData("CD: Archdeacon Holy Garb - boss room after killing boss",
                        "Archdeacon Holy Garb", boss=True, hidden=True),
        DS3LocationData("CD: Archdeacon Skirt - boss room after killing boss", "Archdeacon Skirt",
                        boss=True, hidden=True),
        # Heysel items may not be missable, but it's not clear what causes them to trigger
        DS3LocationData("CD: Heysel Pick - Heysel Corpse-Grub in Rosaria's Bed Chamber",
                        "Heysel Pick", missable=True),
        DS3LocationData("CD: Xanthous Crown - Heysel Corpse-Grub in Rosaria's Bed Chamber",
                        "Xanthous Crown", missable=True),
        DS3LocationData("CD: Deep Ring - upper roofs, passive mob drop in first tower", "Deep Ring",
                        drop=True, hidden=True),
        DS3LocationData("CD: Deep Braille Divine Tome - mimic by side chapel",
                        "Deep Braille Divine Tome", mimic=True),
        DS3LocationData("CD: Red Sign Soapstone - passive mob drop by Rosaria's Bed Chamber",
                        "Red Sign Soapstone", drop=True, hidden=True),
        DS3LocationData("CD: Aldrich's Sapphire - side chapel, miniboss drop", "Aldrich's Sapphire",
                        miniboss=True),  # Deep Accursed Drop
        DS3LocationData("CD: Titanite Scale - moat, miniboss drop", "Titanite Scale",
                        miniboss=True),  # Ravenous Crystal Lizard drop
        DS3LocationData("CD: Twinkling Titanite - moat, lizard #1", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("CD: Twinkling Titanite - moat, lizard #2", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("CD: Rosaria's Fingers - Rosaria", "Rosaria's Fingers",
                        hidden=True),  # Hidden fall
        DS3LocationData("CD -> PW1", None),

        # Longfinger Kirk drops
        DS3LocationData("CD: Barbed Straight Sword - Kirk drop", "Barbed Straight Sword",
                        missable=True, hostile_npc=True),
        DS3LocationData("CD: Spiked Shield - Kirk drop", "Spiked Shield", missable=True,
                        hostile_npc=True),
        # In Rosaria's Bed Chamber
        DS3LocationData("CD: Helm of Thorns - Rosaria's Bed Chamber after killing Kirk",
                        "Helm of Thorns", missable=True, hostile_npc=True),
        DS3LocationData("CD: Armor of Thorns - Rosaria's Bed Chamber after killing Kirk",
                        "Armor of Thorns", missable=True, hostile_npc=True),
        DS3LocationData("CD: Gauntlets of Thorns - Rosaria's Bed Chamber after killing Kirk",
                        "Gauntlets of Thorns", missable=True, hostile_npc=True),
        DS3LocationData("CD: Leggings of Thorns - Rosaria's Bed Chamber after killing Kirk",
                        "Leggings of Thorns", missable=True, hostile_npc=True),

        # Unbreakable Patches
        DS3LocationData("CD: Rusted Coin - don't forgive Patches", "Rusted Coin",
                        missable=True, npc=True),
        DS3LocationData("FS: Rusted Gold Coin - don't forgive Patches", "Rusted Gold Coin",
                        static='99,0:50006201::', missable=True,
                        npc=True),  # Don't forgive Patches
        DS3LocationData("CD: Shotel - Patches", "Shotel", missable=True, npc=True, shop=True),
        DS3LocationData("CD: Ember - Patches", "Ember", missable=True, npc=True, shop=True),
        DS3LocationData("CD: Horsehoof Ring - Patches", "Horsehoof Ring", missable=True,
                        npc=True, drop=True, shop=True),  # (kill or buy)
    ],
    "Farron Keep": [
        DS3LocationData("FK: Lightning Spear - upper keep, far side of the wall",
                        "Lightning Spear"),
        DS3LocationData("FK: Dragon Crest Shield - upper keep, far side of the wall",
                        "Dragon Crest Shield"),
        DS3LocationData("FK: Soul of the Blood of the Wolf", "Soul of the Blood of the Wolf",
                        boss=True),
        DS3LocationData("FK: Cinders of a Lord - Abyss Watcher",
                        "Cinders of a Lord - Abyss Watcher",
                        static="03,0:50002100::", prominent=True, progression=True,
                        boss=True),
        DS3LocationData("FK: Manikin Claws - Londor Pale Shade drop", "Manikin Claws",
                        missable=True, hostile_npc=True,
                        npc=True),  # Londor Pale Shade (if Yoel/Yuria hostile)
        DS3LocationData("FK: Purple Moss Clump - keep ruins, ritual island",
                        "Purple Moss Clump x2"),
        DS3LocationData("FK: Purple Moss Clump - ramp directly in front of Farron Keep bonfire",
                        "Purple Moss Clump x4"),
        DS3LocationData("FK: Greatsword - ramp by keep ruins ritual island", "Greatsword"),
        DS3LocationData("FK: Hollow Gem - perimeter, drop down into swamp", "Hollow Gem",
                        hidden=True),
        DS3LocationData("FK: Purple Moss Clump - Farron Keep bonfire, around right corner",
                        "Purple Moss Clump x3"),
        DS3LocationData("FK: Undead Bone Shard - pavilion by keep ruins bonfire island",
                        "Undead Bone Shard"),
        DS3LocationData("FK: Atonement - perimeter, drop down into swamp", "Atonement",
                        hidden=True),
        DS3LocationData("FK: Titanite Shard - by ladder to keep proper", "Titanite Shard"),
        DS3LocationData("FK: Iron Flesh - Farron Keep bonfire, right after exit", "Iron Flesh"),
        DS3LocationData("FK: Stone Parma - near wall by left island", "Stone Parma"),
        DS3LocationData("FK: Rotten Pine Resin - left island, behind fire", "Rotten Pine Resin x2"),
        DS3LocationData("FK: Titanite Shard - between left island and keep ruins", "Titanite Shard"),
        DS3LocationData("FK: Rusted Gold Coin - right island, behind wall", "Rusted Gold Coin",
                        hidden=True),
        DS3LocationData("FK: Nameless Knight Helm - corner of keep and right island",
                        "Nameless Knight Helm"),
        DS3LocationData("FK: Nameless Knight Armor - corner of keep and right island",
                        "Nameless Knight Armor"),
        DS3LocationData("FK: Nameless Knight Gauntlets - corner of keep and right island",
                        "Nameless Knight Gauntlets"),
        DS3LocationData("FK: Nameless Knight Leggings - corner of keep and right island",
                        "Nameless Knight Leggings"),
        DS3LocationData("FK: Shriving Stone - perimeter, just past stone doors", "Shriving Stone"),
        DS3LocationData("FK: Repair Powder - outside hidden cave", "Repair Powder x4",
                        hidden=True),
        DS3LocationData("FK: Golden Scroll - hidden cave", "Golden Scroll", hidden=True),
        DS3LocationData("FK: Sage's Scroll - near wall by keep ruins bonfire island",
                        "Sage's Scroll"),
        DS3LocationData("FK: Dreamchaser's Ashes - keep proper, illusory wall",
                        "Dreamchaser's Ashes", progression=True, hidden=True),
        DS3LocationData("FK: Titanite Shard - keep ruins bonfire island, under ramp",
                        "Titanite Shard"),
        DS3LocationData("FK: Wolf's Blood Swordgrass - by ladder to keep proper",
                        "Wolf's Blood Swordgrass"),
        DS3LocationData("FK: Great Magic Weapon - perimeter, by door to Road of Sacrifices",
                        "Great Magic Weapon"),
        DS3LocationData("FK: Ember - perimeter, path to boss", "Ember"),
        DS3LocationData("FK: Titanite Shard - swamp by right island", "Titanite Shard x2"),
        DS3LocationData("FK: Titanite Shard - by left island stairs", "Titanite Shard"),
        DS3LocationData("FK: Titanite Shard - by keep ruins ritual island stairs", "Titanite Shard"),
        DS3LocationData("FK: Black Bug Pellet - perimeter, hill by boss door",
                        "Black Bug Pellet x3"),
        DS3LocationData("FK: Rotten Pine Resin - outside pavilion by left island",
                        "Rotten Pine Resin x4"),
        DS3LocationData("FK: Poison Gem - near wall by keep ruins bridge", "Poison Gem"),
        DS3LocationData("FK: Ragged Mask - Farron Keep bonfire, around left corner", "Ragged Mask"),
        DS3LocationData("FK: Estus Shard - between Farron Keep bonfire and left island",
                        "Estus Shard"),
        DS3LocationData("FK: Homeward Bone - right island, behind fire", "Homeward Bone x2"),
        DS3LocationData("FK: Titanite Shard - Farron Keep bonfire, left after exit",
                        "Titanite Shard"),
        DS3LocationData("FK: Large Soul of a Nameless Soldier - corner of keep and right island",
                        "Large Soul of a Nameless Soldier", hidden=True),  # Tricky corner to spot
        DS3LocationData("FK: Prism Stone - by left island stairs", "Prism Stone x10"),
        DS3LocationData("FK: Large Soul of a Nameless Soldier - near wall by right island",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("FK: Sage's Coal - pavilion by left island", "Sage's Coal"),
        DS3LocationData("FK: Gold Pine Bundle - by white tree", "Gold Pine Bundle x6"),
        DS3LocationData("FK: Ember - by white tree", "Ember"),
        DS3LocationData("FK: Soul of a Nameless Soldier - by white tree", "Soul of a Nameless Soldier"),
        DS3LocationData("FK: Large Soul of an Unknown Traveler - by white tree",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("FK: Greataxe - upper keep, by miniboss", "Greataxe"),
        DS3LocationData("FK: Ember - upper keep, by miniboss #1", "Ember"),
        DS3LocationData("FK: Ember - upper keep, by miniboss #2", "Ember"),
        DS3LocationData("FK: Dark Stoneplate Ring+2 - keep ruins ritual island, behind wall",
                        "Dark Stoneplate Ring+2", ngp=True, hidden=True),
        DS3LocationData("FK: Magic Stoneplate Ring+1 - between right island and wall",
                        "Magic Stoneplate Ring+1", ngp=True),
        DS3LocationData("FK: Wolf Ring+1 - keep ruins bonfire island, outside building",
                        "Wolf Ring+1", ngp=True),
        DS3LocationData("FK: Antiquated Dress - hidden cave", "Antiquated Dress", hidden=True),
        DS3LocationData("FK: Antiquated Gloves - hidden cave", "Antiquated Gloves", hidden=True),
        DS3LocationData("FK: Antiquated Skirt - hidden cave", "Antiquated Skirt", hidden=True),
        DS3LocationData("FK: Sunlight Talisman - estus soup island, by ladder to keep proper",
                        "Sunlight Talisman"),
        DS3LocationData("FK: Young White Branch - by white tree #1", "Young White Branch"),
        DS3LocationData("FK: Young White Branch - by white tree #2", "Young White Branch"),
        DS3LocationData("FK: Crown of Dusk - by white tree", "Crown of Dusk"),
        DS3LocationData("FK: Lingering Dragoncrest Ring - by white tree, miniboss drop",
                        "Lingering Dragoncrest Ring", miniboss=True),  # Great Crab drop
        DS3LocationData("FK: Pharis's Hat - miniboss drop, by keep ruins near wall",
                        "Pharis's Hat", miniboss=True),  # Elder Ghru drop
        DS3LocationData("FK: Black Bow of Pharis - miniboss drop, by keep ruins near wall",
                        "Black Bow of Pharis", miniboss=True),  # Elder Ghru drop
        DS3LocationData("FK: Titanite Scale - perimeter, miniboss drop", "Titanite Scale x2",
                        miniboss=True),  # Ravenous Crystal Lizard drop
        DS3LocationData("FK: Large Titanite Shard - upper keep, lizard in open",
                        "Large Titanite Shard", lizard=True),
        DS3LocationData("FK: Large Titanite Shard - upper keep, lizard by wyvern",
                        "Large Titanite Shard", lizard=True),
        DS3LocationData("FK: Heavy Gem - upper keep, lizard on stairs", "Heavy Gem", lizard=True),
        DS3LocationData("FK: Twinkling Titanite - keep proper, lizard", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("FK: Soul of a Stray Demon - upper keep, miniboss drop",
                        "Soul of a Stray Demon", miniboss=True),
        DS3LocationData("FK: Watchdogs of Farron - Old Wolf", "Watchdogs of Farron"),
        DS3LocationData("FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
                        "Hawkwood's Shield", missable=True,
                        npc=True),  # Hawkwood (quest, after Greatwood, Sage, Watchers, and Deacons)
        DS3LocationData("US: Hawk Ring - Giant Archer", "Hawk Ring", drop=True,
                        npc=True),  # Giant archer (kill or quest), here because you need to
        # collect all seven White Branch locations to get it peacefully

        # Hawkwood after killing Abyss Watchers
        DS3LocationData("FS: Farron Ring - Hawkwood", "Farron Ring",
                        missable=True, npc=True),

        # Shrine Handmaid after killing Abyss Watchers
        DS3LocationData("FS: Undead Legion Helm - shop after killing FK boss", "Undead Legion Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Undead Legion Armor - shop after killing FK boss",
                        "Undead Legion Armor", boss=True, shop=True),
        DS3LocationData("FS: Undead Legion Gauntlet - shop after killing FK boss",
                        "Undead Legion Gauntlet", boss=True, shop=True),
        DS3LocationData("FS: Undead Legion Leggings - shop after killing FK boss",
                        "Undead Legion Leggings", boss=True, shop=True),

        # Appears after killing Havel Knight in Archdragon Peak
        DS3LocationData("FK: Havel's Helm - upper keep, after killing AP belfry roof NPC",
                        "Havel's Helm", hidden=True, hostile_npc=True),
        DS3LocationData("FK: Havel's Armor - upper keep, after killing AP belfry roof NPC",
                        "Havel's Armor", hidden=True, hostile_npc=True),
        DS3LocationData("FK: Havel's Gauntlets - upper keep, after killing AP belfry roof NPC",
                        "Havel's Gauntlets", hidden=True, hostile_npc=True),
        DS3LocationData("FK: Havel's Leggings - upper keep, after killing AP belfry roof NPC",
                        "Havel's Leggings", hidden=True, hostile_npc=True),
    ],
    "Catacombs of Carthus": [
        DS3LocationData("CC: Soul of High Lord Wolnir", "Soul of High Lord Wolnir",
                        prominent=True, boss=True),
        DS3LocationData("CC: Carthus Rouge - atrium upper, left after entrance",
                        "Carthus Rouge x2"),
        DS3LocationData("CC: Sharp Gem - atrium lower, right before exit", "Sharp Gem"),
        DS3LocationData("CC: Soul of a Nameless Soldier - atrium lower, down hall",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("CC: Titanite Shard - atrium lower, corner by stairs", "Titanite Shard x2"),
        DS3LocationData("CC: Bloodred Moss Clump - atrium lower, down more stairs",
                        "Bloodred Moss Clump x3"),
        DS3LocationData("CC: Carthus Milkring - crypt upper, among pots", "Carthus Milkring"),
        DS3LocationData("CC: Ember - atrium, on long stairway", "Ember"),
        DS3LocationData("CC: Carthus Rouge - crypt across, corner", "Carthus Rouge x3"),
        DS3LocationData("CC: Ember - crypt upper, end of hall past hole", "Ember"),
        DS3LocationData("CC: Carthus Bloodring - crypt lower, end of side hall", "Carthus Bloodring"),
        DS3LocationData("CC: Titanite Shard - crypt lower, left of entrance", "Titanite Shard x2"),
        DS3LocationData("CC: Titanite Shard - crypt lower, start of side hall", "Titanite Shard x2"),
        DS3LocationData("CC: Ember - crypt lower, shortcut to cavern", "Ember"),
        DS3LocationData("CC: Carthus Pyromancy Tome - atrium lower, jump from bridge",
                        "Carthus Pyromancy Tome",
                        hidden=True),  # Behind illusory wall or hidden drop
        DS3LocationData("CC: Large Titanite Shard - crypt upper, skeleton ball hall",
                        "Large Titanite Shard"),
        DS3LocationData("CC: Large Titanite Shard - crypt across, middle hall",
                        "Large Titanite Shard"),
        DS3LocationData("CC: Yellow Bug Pellet - cavern, on overlook", "Yellow Bug Pellet x3"),
        DS3LocationData("CC: Large Soul of a Nameless Soldier - cavern, before bridge",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("CC: Black Bug Pellet - cavern, before bridge", "Black Bug Pellet x2"),
        DS3LocationData("CC: Grave Warden's Ashes - crypt across, corner", "Grave Warden's Ashes",
                        progression=True),
        DS3LocationData("CC: Large Titanite Shard - tomb lower", "Large Titanite Shard"),
        DS3LocationData("CC: Large Soul of a Nameless Soldier - tomb lower",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("CC: Old Sage's Blindfold - tomb, hall before bonfire",
                        "Old Sage's Blindfold"),
        DS3LocationData("CC: Witch's Ring - tomb, hall before bonfire", "Witch's Ring"),
        DS3LocationData("CC: Soul of a Nameless Soldier - atrium upper, up more stairs",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("CC: Grave Warden Pyromancy Tome - boss arena",
                        "Grave Warden Pyromancy Tome"),
        DS3LocationData("CC: Large Soul of an Unknown Traveler - crypt upper, hall middle",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("CC: Ring of Steel Protection+2 - atrium upper, drop onto pillar",
                        "Ring of Steel Protection+2", ngp=True),
        DS3LocationData("CC: Thunder Stoneplate Ring+1 - crypt upper, among pots",
                        "Thunder Stoneplate Ring+1", ngp=True),
        DS3LocationData("CC: Undead Bone Shard - crypt upper, skeleton ball drop",
                        "Undead Bone Shard", hidden=True),  # Skeleton Ball puzzle
        DS3LocationData("CC: Dark Gem - crypt lower, skeleton ball drop", "Dark Gem",
                        hidden=True),  # Skeleton Ball puzzle
        DS3LocationData("CC: Black Blade - tomb, mimic", "Black Blade", mimic=True),
        DS3LocationData("CC: Soul of a Demon - tomb, miniboss drop", "Soul of a Demon",
                        miniboss=True),
        DS3LocationData("CC: Twinkling Titanite - atrium lower, lizard down more stairs",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("CC: Fire Gem - cavern, lizard", "Fire Gem", lizard=True),
        DS3LocationData("CC: Homeward Bone - Irithyll bridge", "Homeward Bone"),
        DS3LocationData("CC: Pontiff's Right Eye - Irithyll bridge, miniboss drop",
                        "Pontiff's Right Eye", miniboss=True),  # Sulyvahn's Beast drop

        # Shrine Handmaid after killing High Lord Wolnir
        DS3LocationData("FS: Wolnir's Crown - shop after killing CC boss", "Wolnir's Crown",
                        boss=True, shop=True),
    ],
    "Smouldering Lake": [
        DS3LocationData("SL: Soul of the Old Demon King", "Soul of the Old Demon King",
                        prominent=True, boss=True),
        DS3LocationData("SL: Fume Ultra Greatsword - ruins basement, NPC drop",
                        "Fume Ultra Greatsword", hostile_npc=True),  # Knight Slayer Tsorig drop
        DS3LocationData("SL: Black Iron Greatshield - ruins basement, NPC drop",
                        "Black Iron Greatshield", hostile_npc=True),  # Knight Slayer Tsorig drop
        DS3LocationData("SL: Large Titanite Shard - ledge by Demon Ruins bonfire",
                        "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - lake, by entrance", "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - lake, straight from entrance",
                        "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - lake, by tree #1", "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - lake, by miniboss", "Large Titanite Shard"),
        DS3LocationData("SL: Yellow Bug Pellet - side lake", "Yellow Bug Pellet x2"),
        DS3LocationData("SL: Large Titanite Shard - side lake #1", "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - side lake #2", "Large Titanite Shard"),
        DS3LocationData("SL: Large Titanite Shard - lake, by tree #2", "Large Titanite Shard"),
        DS3LocationData("SL: Speckled Stoneplate Ring - lake, ballista breaks bricks",
                        "Speckled Stoneplate Ring", hidden=True),  # Requires careful ballista shot
        DS3LocationData("SL: Homeward Bone - path to ballista", "Homeward Bone x2"),
        DS3LocationData("SL: Ember - ruins main upper, hall end by hole", "Ember"),
        DS3LocationData("SL: Chaos Gem - lake, far end by mob", "Chaos Gem"),
        DS3LocationData("SL: Ember - ruins main lower, path to antechamber", "Ember"),
        DS3LocationData("SL: Izalith Pyromancy Tome - antechamber, room near bonfire",
                        "Izalith Pyromancy Tome"),
        DS3LocationData("SL: Black Knight Sword - ruins main lower, illusory wall in far hall",
                        "Black Knight Sword", hidden=True),
        DS3LocationData("SL: Ember - ruins main upper, just after entrance", "Ember"),
        DS3LocationData("SL: Quelana Pyromancy Tome - ruins main lower, illusory wall in grey room",
                        "Quelana Pyromancy Tome", hidden=True),
        DS3LocationData("SL: Izalith Staff - ruins basement, second illusory wall behind chest",
                        "Izalith Staff", hidden=True),
        DS3LocationData("SL: White Hair Talisman - ruins main lower, in lava",
                        "White Hair Talisman",
                        missable=True),  # This may not even be possible to get without enough fire
        # protection gear which the player may not have
        DS3LocationData("SL: Toxic Mist - ruins main lower, in lava", "Toxic Mist",
                        missable=True),  # This is _probably_ reachable with normal gear, but it
        # still sucks and will probably force a death.
        DS3LocationData("SL: Undead Bone Shard - ruins main lower, left after stairs",
                        "Undead Bone Shard"),
        DS3LocationData("SL: Titanite Scale - ruins basement, path to lava", "Titanite Scale"),
        DS3LocationData("SL: Shield of Want - lake, by miniboss", "Shield of Want"),
        DS3LocationData("SL: Soul of a Crestfallen Knight - ruins basement, above lava",
                        "Soul of a Crestfallen Knight"),

        # Lava items are missable because they require a complex set of armor, rings, spells, and
        # undead bone shards to reliably access without dying.
        DS3LocationData("SL: Ember - ruins basement, in lava", "Ember", missable=True),  # In lava
        DS3LocationData("SL: Sacred Flame - ruins basement, in lava", "Sacred Flame",
                        missable=True),  # In lava

        DS3LocationData("SL: Dragonrider Bow - by ladder from ruins basement to ballista",
                        "Dragonrider Bow", hidden=True),  # Hidden fall
        DS3LocationData("SL: Estus Shard - antechamber, illusory wall", "Estus Shard",
                        hidden=True),
        DS3LocationData("SL: Bloodbite Ring+1 - behind ballista", "Bloodbite Ring+1", ngp=True),
        DS3LocationData("SL: Flame Stoneplate Ring+2 - ruins main lower, illusory wall in far hall",
                        "Flame Stoneplate Ring+2", ngp=True, hidden=True),
        DS3LocationData("SL: Large Titanite Shard - ruins basement, illusory wall in upper hall",
                        "Large Titanite Shard x3", hidden=True),
        DS3LocationData("SL: Undead Bone Shard - lake, miniboss drop", "Undead Bone Shard",
                        miniboss=True),  # Sand Worm drop
        DS3LocationData("SL: Lightning Stake - lake, miniboss drop", "Lightning Stake",
                        miniboss=True),  # Sand Worm drop
        DS3LocationData("SL: Twinkling Titanite - path to side lake, lizard", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("SL: Titanite Chunk - path to side lake, lizard", "Titanite Chunk",
                        lizard=True),
        DS3LocationData("SL: Chaos Gem - antechamber, lizard at end of long hall", "Chaos Gem",
                        lizard=True),
        DS3LocationData("SL: Knight Slayer's Ring - ruins basement, NPC drop",
                        "Knight Slayer's Ring", hostile_npc=True),  # Knight Slayer Tsorig drop

        # Horace the Hushed
        # These are listed here even though you can kill Horace in the Road of Sacrifices because
        # the player may want to complete his and Anri's quest first.
        DS3LocationData("SL: Llewellyn Shield - Horace drop", "Llewellyn Shield", npc=True,
                        hostile_npc=True),
        DS3LocationData("FS: Executioner Helm - shop after killing Horace", "Executioner Helm",
                        npc=True, hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Executioner Armor - shop after killing Horace", "Executioner Armor",
                        npc=True, hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Executioner Gauntlets - shop after killing Horace",
                        "Executioner Gauntlets", hostile_npc=True, npc=True, shop=True,
                        hidden=True),
        DS3LocationData("FS: Executioner Leggings - shop after killing Horace",
                        "Executioner Leggings", hostile_npc=True, npc=True, shop=True,
                        hidden=True),

        # Shrine Handmaid after killing Knight Slayer Tsorig
        DS3LocationData("FS: Black Iron Helm - shop after killing Tsorig", "Black Iron Helm",
                        hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Black Iron Armor - shop after killing Tsorig", "Black Iron Armor",
                        hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Black Iron Gauntlets - shop after killing Tsorig",
                        "Black Iron Gauntlets", hostile_npc=True, shop=True, hidden=True),
        DS3LocationData("FS: Black Iron Leggings - shop after killing Tsorig",
                        "Black Iron Leggings", hostile_npc=True, shop=True, hidden=True),

        # Near Cornyx's cage after killing Old Demon King with Cuculus
        DS3LocationData("US: Spotted Whip - by Cornyx's cage after Cuculus quest", "Spotted Whip",
                        missable=True, boss=True, npc=True),
        DS3LocationData("US: Cornyx's Garb - by Cornyx's cage after Cuculus quest",
                        "Cornyx's Garb", static='02,0:53100100::', missable=True, boss=True,
                        npc=True),
        DS3LocationData("US: Cornyx's Wrap - by Cornyx's cage after Cuculus quest", "Cornyx's Wrap",
                        static='02,0:53100100::', missable=True, boss=True, npc=True),
        DS3LocationData("US: Cornyx's Skirt - by Cornyx's cage after Cuculus quest",
                        "Cornyx's Skirt", static='02,0:53100100::', missable=True, boss=True,
                        npc=True),
    ],
    "Irithyll of the Boreal Valley": [
        DS3LocationData("IBV: Soul of Pontiff Sulyvahn", "Soul of Pontiff Sulyvahn",
                        prominent=True, boss=True),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier - central, by bonfire",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("IBV: Large Titanite Shard - ascent, down ladder in last building",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Soul of a Weary Warrior - central, by first fountain",
                        "Soul of a Weary Warrior"),
        DS3LocationData("IBV: Soul of a Weary Warrior - central, railing by first fountain",
                        "Soul of a Weary Warrior"),
        DS3LocationData("IBV: Rime-blue Moss Clump - central, by bonfire", "Rime-blue Moss Clump"),
        DS3LocationData("IBV: Witchtree Branch - by Dorhys", "Witchtree Branch",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("IBV: Large Titanite Shard - central, side path after first fountain",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Budding Green Blossom - central, by second fountain",
                        "Budding Green Blossom"),
        DS3LocationData("IBV: Rime-blue Moss Clump - central, past second fountain",
                        "Rime-blue Moss Clump x2"),
        DS3LocationData("IBV: Large Titanite Shard - central, balcony just before plaza",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Large Titanite Shard - path to Dorhys", "Large Titanite Shard",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("IBV: Ring of the Sun's First Born - fall from in front of cathedral",
                        "Ring of the Sun's First Born",
                        hidden=True),  # Hidden fall
        DS3LocationData("IBV: Large Soul of a Nameless Soldier - path to plaza",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("IBV: Large Titanite Shard - plaza, balcony overlooking ascent",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Large Titanite Shard - plaza, by stairs to church",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Soul of a Weary Warrior - plaza, side room lower",
                        "Soul of a Weary Warrior"),
        DS3LocationData("IBV: Magic Clutch Ring - plaza, illusory wall", "Magic Clutch Ring",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("IBV: Fading Soul - descent, cliff edge #1", "Fading Soul"),
        DS3LocationData("IBV: Fading Soul - descent, cliff edge #2", "Fading Soul"),
        DS3LocationData("IBV: Homeward Bone - descent, before gravestone", "Homeward Bone x3"),
        DS3LocationData("IBV: Undead Bone Shard - descent, behind gravestone", "Undead Bone Shard",
                        hidden=True),  # Hidden behind gravestone
        DS3LocationData("IBV: Kukri - descent, side path", "Kukri x8"),
        DS3LocationData("IBV: Rusted Gold Coin - descent, side path", "Rusted Gold Coin"),
        DS3LocationData("IBV: Blue Bug Pellet - descent, dark room", "Blue Bug Pellet x2"),
        DS3LocationData("IBV: Shriving Stone - descent, dark room rafters", "Shriving Stone"),
        DS3LocationData("IBV: Blood Gem - descent, platform before lake", "Blood Gem"),
        DS3LocationData("IBV: Green Blossom - lake, by stairs from descent", "Green Blossom x3"),
        DS3LocationData("IBV: Ring of Sacrifice - lake, right of stairs from descent",
                        "Ring of Sacrifice"),
        DS3LocationData("IBV: Great Heal - lake, dead Corpse-Grub", "Great Heal"),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier - lake island",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("IBV: Green Blossom - lake wall", "Green Blossom x3"),
        DS3LocationData("IBV: Dung Pie - sewer #1", "Dung Pie x3"),
        DS3LocationData("IBV: Dung Pie - sewer #2", "Dung Pie x3"),
        # These don't actually guard any single item sales. Maybe we can inject one manually?
        DS3LocationData("IBV: Excrement-covered Ashes - sewer, by stairs",
                        "Excrement-covered Ashes"),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier - ascent, after great hall",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("IBV: Soul of a Weary Warrior - ascent, by final staircase",
                        "Soul of a Weary Warrior"),
        DS3LocationData("IBV: Large Titanite Shard - ascent, by elevator door",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Blue Bug Pellet - ascent, in last building", "Blue Bug Pellet x2"),
        DS3LocationData("IBV: Ember - shortcut from church to cathedral", "Ember"),
        DS3LocationData("IBV: Green Blossom - lake, by Distant Manor", "Green Blossom"),
        DS3LocationData("IBV: Lightning Gem - plaza center", "Lightning Gem"),
        DS3LocationData("IBV: Large Soul of a Nameless Soldier - central, by second fountain",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("IBV: Soul of a Weary Warrior - plaza, side room upper",
                        "Soul of a Weary Warrior"),
        DS3LocationData("IBV: Proof of a Concord Kept - Church of Yorshka altar",
                        "Proof of a Concord Kept"),
        DS3LocationData("IBV: Rusted Gold Coin - Distant Manor, drop after stairs",
                        "Rusted Gold Coin"),
        DS3LocationData("IBV: Chloranthy Ring+1 - plaza, behind altar", "Chloranthy Ring+1",
                        ngp=True),
        DS3LocationData("IBV: Covetous Gold Serpent Ring+1 - descent, drop after dark room",
                        "Covetous Gold Serpent Ring+1", ngp=True, hidden=True),  # Hidden fall
        DS3LocationData("IBV: Wood Grain Ring+2 - ascent, right after great hall", "Wood Grain Ring+2",
                        ngp=True),
        DS3LocationData("IBV: Divine Blessing - great hall, chest", "Divine Blessing"),
        DS3LocationData("IBV: Smough's Great Hammer - great hall, chest",
                        "Smough's Great Hammer"),
        DS3LocationData("IBV: Yorshka's Spear - descent, dark room rafters chest", "Yorshka's Spear"),
        DS3LocationData("IBV: Leo Ring - great hall, chest", "Leo Ring"),
        DS3LocationData("IBV: Dorhys' Gnawing - Dorhys drop", "Dorhys' Gnawing",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("IBV: Divine Blessing - great hall, mob drop",
                        "Divine Blessing", drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard - great hall, main floor mob drop",
                        "Large Titanite Shard", drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard - great hall, upstairs mob drop #1",
                        "Large Titanite Shard x2", drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Large Titanite Shard - great hall, upstairs mob drop #2",
                        "Large Titanite Shard x2", drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Silver Knight
        DS3LocationData("IBV: Roster of Knights - descent, first landing", "Roster of Knights"),
        DS3LocationData("IBV: Twinkling Titanite - descent, lizard behind illusory wall",
                        "Twinkling Titanite", lizard=True, hidden=True),  # Behind illusory wall
        DS3LocationData("IBV: Twinkling Titanite - central, lizard before plaza",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("IBV: Large Titanite Shard - Distant Manor, under overhang",
                        "Large Titanite Shard"),
        DS3LocationData("IBV: Siegbräu - Siegward", "Siegbräu", missable=True, npc=True),
        DS3LocationData("IBV: Emit Force - Siegward", "Emit Force", missable=True, npc=True),
        DS3LocationData("IBV -> ID", None),

        # After winning both Londor Pale Shade invasions
        DS3LocationData("FS: Sneering Mask - Yoel's room, kill Londor Pale Shade twice",
                        "Sneering Mask", missable=True, hostile_npc=True),
        DS3LocationData("FS: Pale Shade Robe - Yoel's room, kill Londor Pale Shade twice",
                        "Pale Shade Robe", missable=True, hostile_npc=True),
        DS3LocationData("FS: Pale Shade Gloves - Yoel's room, kill Londor Pale Shade twice",
                        "Pale Shade Gloves", missable=True, hostile_npc=True),
        DS3LocationData("FS: Pale Shade Trousers - Yoel's room, kill Londor Pale Shade twice",
                        "Pale Shade Trousers", missable=True, hostile_npc=True),

        # Anri of Astora
        DS3LocationData("IBV: Ring of the Evil Eye - Anri", "Ring of the Evil Eye", missable=True,
                        npc=True),

        # Sirris quest after killing Creighton
        DS3LocationData("FS: Mail Breaker - Sirris for killing Creighton", "Mail Breaker",
                        static='99,0:50006080::', missable=True, hostile_npc=True,
                        npc=True),
        DS3LocationData("FS: Silvercat Ring - Sirris for killing Creighton", "Silvercat Ring",
                        missable=True, hostile_npc=True, npc=True),
        DS3LocationData("IBV: Dragonslayer's Axe - Creighton drop", "Dragonslayer's Axe",
                        missable=True, hostile_npc=True, npc=True),
        DS3LocationData("IBV: Creighton's Steel Mask - bridge after killing Creighton",
                        "Creighton's Steel Mask", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("IBV: Mirrah Chain Mail - bridge after killing Creighton",
                        "Mirrah Chain Mail", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("IBV: Mirrah Chain Gloves - bridge after killing Creighton",
                        "Mirrah Chain Gloves", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("IBV: Mirrah Chain Leggings - bridge after killing Creighton",
                        "Mirrah Chain Leggings", missable=True, hostile_npc=True, npc=True),
    ],
    "Irithyll Dungeon": [
        DS3LocationData("ID: Titanite Slab - Siegward", "Titanite Slab", missable=True,
                        npc=True),
        DS3LocationData("ID: Murakumo - Alva drop", "Murakumo", missable=True,
                        hostile_npc=True),
        DS3LocationData("ID: Large Titanite Shard - after bonfire, second cell on left",
                        "Large Titanite Shard"),
        DS3LocationData("ID: Fading Soul - B1 near, main hall", "Fading Soul"),
        DS3LocationData("ID: Large Soul of a Nameless Soldier - B2, hall by stairs",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("ID: Jailbreaker's Key - B1 far, cell after gate", "Jailbreaker's Key"),
        DS3LocationData("ID: Pale Pine Resin - B1 far, cell with broken wall",
                        "Pale Pine Resin x2"),
        DS3LocationData("ID: Simple Gem - B2 far, cell by stairs", "Simple Gem"),
        DS3LocationData("ID: Large Soul of a Nameless Soldier - B2 far, by lift",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("ID: Large Titanite Shard - B1 far, rightmost cell",
                        "Large Titanite Shard"),
        DS3LocationData("ID: Homeward Bone - path from B2 to pit", "Homeward Bone x2"),
        DS3LocationData("ID: Bellowing Dragoncrest Ring - drop from B1 towards pit",
                        "Bellowing Dragoncrest Ring", conditional=True),
        DS3LocationData("ID: Soul of a Weary Warrior - by drop to pit", "Soul of a Weary Warrior"),
        DS3LocationData("ID: Soul of a Crestfallen Knight - balcony above pit",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("ID: Lightning Bolt - awning over pit", "Lightning Bolt x9"),
        DS3LocationData("ID: Large Titanite Shard - pit #1", "Large Titanite Shard"),
        DS3LocationData("ID: Profaned Flame - pit", "Profaned Flame"),
        DS3LocationData("ID: Large Titanite Shard - pit #2", "Large Titanite Shard"),
        DS3LocationData("ID: Soul of a Weary Warrior - stairs between pit and B3",
                        "Soul of a Weary Warrior"),
        DS3LocationData("ID: Dung Pie - B3, by path from pit", "Dung Pie x4"),
        DS3LocationData("ID: Ember - B3 center", "Ember"),
        DS3LocationData("ID: Ember - B3 far right", "Ember"),
        DS3LocationData("ID: Profaned Coal - B3 far, left cell", "Profaned Coal"),
        DS3LocationData("ID: Large Titanite Shard - B3 near, right corner", "Large Titanite Shard"),
        DS3LocationData("ID: Old Sorcerer Hat - B2 near, middle cell", "Old Sorcerer Hat"),
        DS3LocationData("ID: Old Sorcerer Coat - B2 near, middle cell", "Old Sorcerer Coat"),
        DS3LocationData("ID: Old Sorcerer Gauntlets - B2 near, middle cell",
                        "Old Sorcerer Gauntlets"),
        DS3LocationData("ID: Old Sorcerer Boots - B2 near, middle cell", "Old Sorcerer Boots"),
        DS3LocationData("ID: Large Soul of a Weary Warrior - just before Profaned Capital",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("ID: Covetous Gold Serpent Ring - Siegward's cell",
                        "Covetous Gold Serpent Ring", conditional=True),
        DS3LocationData("ID: Lightning Blade - B3 lift, middle platform", "Lightning Blade"),
        DS3LocationData("ID: Rusted Coin - after bonfire, first cell on left", "Rusted Coin"),
        DS3LocationData("ID: Dusk Crown Ring - B3 far, right cell", "Dusk Crown Ring"),
        DS3LocationData("ID: Pickaxe - path from pit to B3", "Pickaxe"),
        DS3LocationData("ID: Xanthous Ashes - B3 far, right cell", "Xanthous Ashes",
                        progression=True),
        DS3LocationData("ID: Large Titanite Shard - B1 near, by door", "Large Titanite Shard"),
        DS3LocationData("ID: Rusted Gold Coin - after bonfire, last cell on right",
                        "Rusted Gold Coin"),
        DS3LocationData("ID: Old Cell Key - stairs between pit and B3", "Old Cell Key"),
        DS3LocationData("ID: Covetous Silver Serpent Ring+1 - pit lift, middle platform",
                        "Covetous Silver Serpent Ring+1", ngp=True),
        DS3LocationData("ID: Dragon Torso Stone - B3, outside lift", "Dragon Torso Stone"),
        DS3LocationData("ID: Prisoner Chief's Ashes - B2 near, locked cell by stairs",
                        "Prisoner Chief's Ashes", progression=True),
        DS3LocationData("ID: Great Magic Shield - B2 near, mob drop in far left cell",
                        "Great Magic Shield", drop=True,
                        hidden=True),  # Guaranteed drop from a normal-looking Corpse-Grub
        DS3LocationData("ID: Dragonslayer Lightning Arrow - pit, mimic in hall",
                        "Dragonslayer Lightning Arrow x10", mimic=True),
        DS3LocationData("ID: Titanite Scale - B3 far, mimic in hall", "Titanite Scale x2",
                        mimic=True),
        DS3LocationData("ID: Dark Clutch Ring - stairs between pit and B3, mimic",
                        "Dark Clutch Ring", mimic=True),
        DS3LocationData("ID: Estus Shard - mimic on path from B2 to pit", "Estus Shard",
                        mimic=True),
        DS3LocationData("ID: Titanite Chunk - balcony above pit, lizard", "Titanite Chunk",
                        lizard=True),
        DS3LocationData("ID: Titanite Scale - B2 far, lizard", "Titanite Scale", lizard=True),

        # These are missable because of a bug that causes them to be dropped wherever the giant is
        # randomized to, instead of where the miniboss is in vanilla.
        DS3LocationData("ID: Dung Pie - pit, miniboss drop", "Dung Pie x4",
                        miniboss=True, missable=True),  # Giant slave drop
        DS3LocationData("ID: Titanite Chunk - pit, miniboss drop", "Titanite Chunk",
                        miniboss=True, missable=True),  # Giant Slave Drop

        # Alva (requires ember)
        DS3LocationData("ID: Alva Helm - B3 near, by Karla's cell, after killing Alva", "Alva Helm",
                        missable=True, npc=True),
        DS3LocationData("ID: Alva Armor - B3 near, by Karla's cell, after killing Alva",
                        "Alva Armor", missable=True, npc=True),
        DS3LocationData("ID: Alva Gauntlets - B3 near, by Karla's cell, after killing Alva",
                        "Alva Gauntlets", missable=True, npc=True),
        DS3LocationData("ID: Alva Leggings - B3 near, by Karla's cell, after killing Alva",
                        "Alva Leggings", missable=True, npc=True),
    ],
    "Profaned Capital": [
        DS3LocationData("PC: Soul of Yhorm the Giant", "Soul of Yhorm the Giant", boss=True),
        DS3LocationData("PC: Cinders of a Lord - Yhorm the Giant",
                        "Cinders of a Lord - Yhorm the Giant", static="07,0:50002170::",
                        prominent=True, progression=True, boss=True),
        DS3LocationData("PC: Logan's Scroll - chapel roof, NPC drop", "Logan's Scroll",
                        hostile_npc=True),  # Sorcerer
        DS3LocationData("PC: Purging Stone - chapel ground floor", "Purging Stone x3"),
        DS3LocationData("PC: Rusted Coin - tower exterior", "Rusted Coin x2"),
        DS3LocationData("PC: Rusted Gold Coin - halls above swamp", "Rusted Gold Coin"),
        DS3LocationData("PC: Purging Stone - swamp, by chapel ladder", "Purging Stone"),
        DS3LocationData("PC: Cursebite Ring - swamp, below halls", "Cursebite Ring"),
        DS3LocationData("PC: Poison Gem - swamp, below halls", "Poison Gem"),
        DS3LocationData("PC: Shriving Stone - swamp, by chapel door", "Shriving Stone"),
        DS3LocationData("PC: Poison Arrow - chapel roof", "Poison Arrow x18"),
        DS3LocationData("PC: Rubbish - chapel, down stairs from second floor", "Rubbish"),
        DS3LocationData("PC: Onislayer Greatarrow - bridge", "Onislayer Greatarrow x8"),
        DS3LocationData("PC: Large Soul of a Weary Warrior - bridge, far end",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("PC: Rusted Coin - below bridge #1", "Rusted Coin"),
        DS3LocationData("PC: Rusted Coin - below bridge #2", "Rusted Coin"),
        DS3LocationData("PC: Blooming Purple Moss Clump - walkway above swamp",
                        "Blooming Purple Moss Clump x3"),
        DS3LocationData("PC: Wrath of the Gods - chapel, drop from roof", "Wrath of the Gods"),
        DS3LocationData("PC: Onislayer Greatbow - drop from bridge", "Onislayer Greatbow",
                        hidden=True),  # Hidden fall
        DS3LocationData("PC: Jailer's Key Ring - hall past chapel", "Jailer's Key Ring",
                        progression=True),
        DS3LocationData("PC: Ember - palace, far room", "Ember"),
        DS3LocationData("PC: Flame Stoneplate Ring+1 - chapel, drop from roof towards entrance",
                        "Flame Stoneplate Ring+1", ngp=True, hidden=True),  # Hidden fall
        DS3LocationData("PC: Magic Stoneplate Ring+2 - tower base", "Magic Stoneplate Ring+2",
                        ngp=True),
        DS3LocationData("PC: Court Sorcerer Hood - chapel, second floor", "Court Sorcerer Hood"),
        DS3LocationData("PC: Court Sorcerer Robe - chapel, second floor", "Court Sorcerer Robe"),
        DS3LocationData("PC: Court Sorcerer Gloves - chapel, second floor", "Court Sorcerer Gloves"),
        DS3LocationData("PC: Court Sorcerer Trousers - chapel, second floor",
                        "Court Sorcerer Trousers"),
        DS3LocationData("PC: Storm Ruler - boss room", "Storm Ruler"),
        DS3LocationData("PC: Undead Bone Shard - by bonfire", "Undead Bone Shard"),
        DS3LocationData("PC: Eleonora - chapel ground floor, kill mob", "Eleonora",
                        drop=True,
                        hidden=True),  # Guaranteed drop from a normal-looking Monstrosity of Sin
        DS3LocationData("PC: Rusted Gold Coin - palace, mimic in far room", "Rusted Gold Coin x2",
                        mimic=True),
        DS3LocationData("PC: Court Sorcerer's Staff - chapel, mimic on second floor",
                        "Court Sorcerer's Staff", mimic=True),
        DS3LocationData("PC: Greatshield of Glory - palace, mimic in far room",
                        "Greatshield of Glory", mimic=True),
        DS3LocationData("PC: Twinkling Titanite - halls above swamp, lizard #1",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("PC: Twinkling Titanite - halls above swamp, lizard #2",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("PC: Siegbräu - Siegward after killing boss", "Siegbräu",
                        missable=True, npc=True),

        # Siegward drops (kill or quest)
        DS3LocationData("PC: Storm Ruler - Siegward", "Storm Ruler", static='02,0:50006218::',
                        missable=True, drop=True, npc=True),
        DS3LocationData("PC: Pierce Shield - Siegward", "Pierce Shield", missable=True,
                        drop=True, npc=True),
    ],
    # We consider "Anor Londo" to be everything accessible only after killing Pontiff. This doesn't
    # match up one-to-one with where the game pops up the region name, but it balances items better
    # and covers the region that's full of DS1 Anor Londo references.
    "Anor Londo": [
        DS3LocationData("AL: Soul of Aldrich", "Soul of Aldrich", boss=True),
        DS3LocationData("AL: Cinders of a Lord - Aldrich", "Cinders of a Lord - Aldrich",
                        static='06,0:50002130::', prominent=True, progression=True,
                        boss=True),
        DS3LocationData("AL: Yorshka's Chime - kill Yorshka", "Yorshka's Chime", missable=True,
                        drop=True,
                        npc=True),  # Hidden walkway, missable because it will break Sirris's quest
        DS3LocationData("AL: Drang Twinspears - plaza, NPC drop", "Drang Twinspears", drop=True,
                        hidden=True),
        DS3LocationData("AL: Estus Shard - dark cathedral, by left stairs", "Estus Shard"),
        DS3LocationData("AL: Painting Guardian's Curved Sword - prison tower rafters",
                        "Painting Guardian's Curved Sword", hidden=True),  # Invisible walkway
        DS3LocationData("AL: Brass Helm - tomb", "Brass Helm",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Brass Armor - tomb", "Brass Armor",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Brass Gauntlets - tomb", "Brass Gauntlets",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Brass Leggings - tomb", "Brass Leggings",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Human Dregs - water reserves", "Human Dregs",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Ember - spiral staircase, bottom", "Ember"),
        DS3LocationData("AL: Large Titanite Shard - bottom of the furthest buttress",
                        "Large Titanite Shard"),
        DS3LocationData("AL: Large Titanite Shard - right after light cathedral",
                        "Large Titanite Shard"),
        DS3LocationData("AL: Large Titanite Shard - walkway, side path by cathedral",
                        "Large Titanite Shard"),
        DS3LocationData("AL: Soul of a Weary Warrior - plaza, nearer", "Soul of a Weary Warrior"),
        DS3LocationData("AL: Ember - plaza, right side", "Ember"),
        DS3LocationData("AL: Ember - plaza, further", "Ember"),
        DS3LocationData("AL: Large Titanite Shard - balcony by dead giants",
                        "Large Titanite Shard"),
        DS3LocationData("AL: Dark Stoneplate Ring - by dark stairs up from plaza",
                        "Dark Stoneplate Ring"),
        DS3LocationData("AL: Large Titanite Shard - bottom of the nearest buttress",
                        "Large Titanite Shard"),
        DS3LocationData("AL: Deep Gem - water reserves", "Deep Gem"),
        DS3LocationData("AL: Titanite Scale - top of ladder up to buttresses", "Titanite Scale"),
        DS3LocationData("AL: Dragonslayer Greatarrow - drop from nearest buttress",
                        "Dragonslayer Greatarrow x5", static='06,0:53700620::',
                        hidden=True),  # Hidden fall
        DS3LocationData("AL: Dragonslayer Greatbow - drop from nearest buttress",
                        "Dragonslayer Greatbow", static='06,0:53700620::',
                        hidden=True),  # Hidden fall
        DS3LocationData("AL: Easterner's Ashes - below top of furthest buttress",
                        "Easterner's Ashes", progression=True),
        DS3LocationData("AL: Painting Guardian Hood - prison tower, rafters",
                        "Painting Guardian Hood", hidden=True),  # Invisible walkway
        DS3LocationData("AL: Painting Guardian Gown - prison tower, rafters",
                        "Painting Guardian Gown", hidden=True),  # Invisible walkway
        DS3LocationData("AL: Painting Guardian Gloves - prison tower, rafters",
                        "Painting Guardian Gloves", hidden=True),  # Invisible walkway
        DS3LocationData("AL: Painting Guardian Waistcloth - prison tower, rafters",
                        "Painting Guardian Waistcloth", hidden=True),  # Invisible walkway
        DS3LocationData("AL: Soul of a Crestfallen Knight - right of dark cathedral entrance",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("AL: Moonlight Arrow - dark cathedral, up right stairs",
                        "Moonlight Arrow x6"),
        DS3LocationData("AL: Proof of a Concord Kept - dark cathedral, up left stairs",
                        "Proof of a Concord Kept"),
        DS3LocationData("AL: Large Soul of a Weary Warrior - left of dark cathedral entrance",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("AL: Giant's Coal - by giant near dark cathedral", "Giant's Coal"),
        DS3LocationData("AL: Havel's Ring+2 - prison tower, rafters", "Havel's Ring+2", ngp=True,
                        hidden=True),  # Invisible walkway
        DS3LocationData("AL: Ring of Favor+1 - light cathedral, upstairs", "Ring of Favor+1",
                        ngp=True),
        DS3LocationData("AL: Sun Princess Ring - dark cathedral, after boss", "Sun Princess Ring"),
        DS3LocationData("AL: Reversal Ring - tomb, chest in corner", "Reversal Ring",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("AL: Golden Ritual Spear - light cathedral, mimic upstairs",
                        "Golden Ritual Spear", mimic=True),
        DS3LocationData("AL: Ring of Favor - water reserves, both minibosses", "Ring of Favor",
                        miniboss=True,
                        hidden=True),  # Sulyvahn's Beast Duo drop, behind illusory wall
        DS3LocationData("AL: Blade of the Darkmoon - Yorshka with Darkmoon Loyalty",
                        "Blade of the Darkmoon", missable=True, drop=True,
                        npc=True),  # Hidden walkway, missable because it will break Sirris's quest
        DS3LocationData("AL: Simple Gem - light cathedral, lizard upstairs", "Simple Gem",
                        lizard=True),
        DS3LocationData("AL: Twinkling Titanite - lizard after light cathedral #1",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("AL: Twinkling Titanite - lizard after light cathedral #2",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("AL: Aldrich's Ruby - dark cathedral, miniboss", "Aldrich's Ruby",
                        miniboss=True, missable=True),  # Deep Accursed drop, missable after defeating Aldrich
        DS3LocationData("AL: Aldrich Faithful - water reserves, talk to McDonnel", "Aldrich Faithful",
                        hidden=True),  # Behind illusory wall

        DS3LocationData("FS: Budding Green Blossom - shop after killing Creighton and AL boss",
                        "Budding Green Blossom", static='99,0:-1:110000,70000118:',
                        missable=True, npc=True,
                        shop=True),  # sold by Shrine Maiden after killing Aldrich and helping
        # Sirris defeat Creighton

        # Sirris (quest completion)
        DS3LocationData("FS: Sunset Shield - by grave after killing Hodrick w/Sirris",
                        "Sunset Shield", missable=True, hostile_npc=True, npc=True),
        # In Pit of Hollows after killing Hodrick
        DS3LocationData("US: Sunset Helm - Pit of Hollows after killing Hodrick w/Sirris",
                        "Sunset Helm", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("US: Sunset Armor - pit of hollows after killing Hodrick w/Sirris",
                        "Sunset Armor", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("US: Sunset Gauntlets - pit of hollows after killing Hodrick w/Sirris",
                        "Sunset Gauntlets", missable=True, hostile_npc=True, npc=True),
        DS3LocationData("US: Sunset Leggings - pit of hollows after killing Hodrick w/Sirris",
                        "Sunset Leggings", missable=True, hostile_npc=True, npc=True),

        # Shrine Handmaid after killing Sulyvahn's Beast Duo
        DS3LocationData("FS: Helm of Favor - shop after killing water reserve minibosses",
                        "Helm of Favor", hidden=True, miniboss=True, shop=True),
        DS3LocationData("FS: Embraced Armor of Favor - shop after killing water reserve minibosses",
                        "Embraced Armor of Favor", hidden=True, miniboss=True, shop=True),
        DS3LocationData("FS: Gauntlets of Favor - shop after killing water reserve minibosses",
                        "Gauntlets of Favor", hidden=True, miniboss=True, shop=True),
        DS3LocationData("FS: Leggings of Favor - shop after killing water reserve minibosses",
                        "Leggings of Favor", hidden=True, miniboss=True, shop=True),

        # Anri of Astora
        DS3LocationData("AL: Chameleon - tomb after marrying Anri", "Chameleon", missable=True,
                        npc=True),
        DS3LocationData("AL: Anri's Straight Sword - Anri quest", "Anri's Straight Sword",
                        missable=True, npc=True),

        # Shrine Handmaid after killing Ringfinger Leonhard
        # This is listed here even though you can kill Leonhard immediately because we want the
        # logic to assume people will do his full quest. Missable because he can disappear forever
        # if you use up all your Pale Tongues.
        DS3LocationData("FS: Leonhard's Garb - shop after killing Leonhard",
                        "Leonhard's Garb", hidden=True, npc=True, shop=True, missable=True),
        DS3LocationData("FS: Leonhard's Gauntlets - shop after killing Leonhard",
                        "Leonhard's Gauntlets", hidden=True, npc=True, shop=True,
                        missable=True),
        DS3LocationData("FS: Leonhard's Trousers - shop after killing Leonhard",
                        "Leonhard's Trousers", hidden=True, npc=True, shop=True,
                        missable=True),

        # Shrine Handmaid after killing Alrich, Devourer of Gods
        DS3LocationData("FS: Smough's Helm - shop after killing AL boss", "Smough's Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Smough's Armor - shop after killing AL boss", "Smough's Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Smough's Gauntlets - shop after killing AL boss", "Smough's Gauntlets",
                        boss=True, shop=True),
        DS3LocationData("FS: Smough's Leggings - shop after killing AL boss", "Smough's Leggings",
                        boss=True, shop=True),

        # Ringfinger Leonhard (quest or kill)
        DS3LocationData("AL: Crescent Moon Sword - Leonhard drop", "Crescent Moon Sword",
                        missable=True, npc=True),
        DS3LocationData("AL: Silver Mask - Leonhard drop", "Silver Mask", missable=True,
                        npc=True),
        DS3LocationData("AL: Soul of Rosaria - Leonhard drop", "Soul of Rosaria", missable=True,
                        npc=True),

        # Shrine Handmaid after killing Anri or completing their quest
        DS3LocationData("FS: Elite Knight Helm - shop after Anri quest", "Elite Knight Helm",
                        npc=True, shop=True),
        DS3LocationData("FS: Elite Knight Armor - shop after Anri quest", "Elite Knight Armor",
                        npc=True, shop=True),
        DS3LocationData("FS: Elite Knight Gauntlets - shop after Anri quest",
                        "Elite Knight Gauntlets", npc=True, shop=True),
        DS3LocationData("FS: Elite Knight Leggings - shop after Anri quest",
                        "Elite Knight Leggings", npc=True, shop=True),
    ],
    "Lothric Castle": [
        DS3LocationData("LC: Soul of Dragonslayer Armour", "Soul of Dragonslayer Armour",
                        prominent=True, boss=True),
        DS3LocationData("LC: Sniper Bolt - moat, right path end", "Sniper Bolt x11"),
        DS3LocationData("LC: Sniper Crossbow - moat, right path end", "Sniper Crossbow"),
        DS3LocationData("LC: Titanite Scale - dark room, upper balcony", "Titanite Scale"),
        DS3LocationData("LC: Titanite Chunk - dark room mid, out door opposite wyvern",
                        "Titanite Chunk"),
        DS3LocationData("LC: Greatlance - overlooking Dragon Barracks bonfire", "Greatlance"),
        DS3LocationData("LC: Titanite Chunk - ascent, first balcony", "Titanite Chunk"),
        DS3LocationData("LC: Titanite Chunk - ascent, turret before barricades", "Titanite Chunk"),
        DS3LocationData("LC: Sacred Bloom Shield - ascent, behind illusory wall",
                        "Sacred Bloom Shield", hidden=True),  # Behind illusory wall
        DS3LocationData("LC: Titanite Chunk - ascent, final turret", "Titanite Chunk x2"),
        DS3LocationData("LC: Refined Gem - plaza", "Refined Gem"),
        DS3LocationData("LC: Soul of a Crestfallen Knight - by lift bottom",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("LC: Undead Bone Shard - moat, far ledge", "Undead Bone Shard"),
        DS3LocationData("LC: Lightning Urn - moat, right path, first room", "Lightning Urn x3"),
        DS3LocationData("LC: Titanite Chunk - moat #1", "Titanite Chunk"),
        DS3LocationData("LC: Titanite Chunk - moat #2", "Titanite Chunk"),
        DS3LocationData("LC: Titanite Chunk - moat, near ledge", "Titanite Chunk"),
        DS3LocationData("LC: Caitha's Chime - chapel, drop onto roof", "Caitha's Chime"),
        DS3LocationData("LC: Lightning Urn - plaza", "Lightning Urn x6"),
        DS3LocationData("LC: Ember - plaza, by gate", "Ember"),
        DS3LocationData("LC: Raw Gem - plaza left", "Raw Gem"),
        DS3LocationData("LC: Black Firebomb - dark room lower", "Black Firebomb x3"),
        DS3LocationData("LC: Pale Pine Resin - dark room upper, by mimic", "Pale Pine Resin"),
        DS3LocationData("LC: Large Soul of a Weary Warrior - main hall, by lever",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("LC: Sunlight Medal - by lift top", "Sunlight Medal"),
        DS3LocationData("LC: Soul of a Crestfallen Knight - wyvern room, balcony",
                        "Soul of a Crestfallen Knight", hidden=True),  # Hidden fall
        DS3LocationData("LC: Titanite Chunk - altar roof", "Titanite Chunk"),
        DS3LocationData("LC: Titanite Scale - dark room mid, out door opposite wyvern",
                        "Titanite Scale"),
        DS3LocationData("LC: Large Soul of a Nameless Soldier - moat, right path",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("LC: Knight's Ring - altar", "Knight's Ring"),
        DS3LocationData("LC: Ember - main hall, left of stairs", "Ember"),
        DS3LocationData("LC: Large Soul of a Weary Warrior - ascent, last turret",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("LC: Ember - by Dragon Barracks bonfire", "Ember"),
        DS3LocationData("LC: Twinkling Titanite - ascent, side room", "Twinkling Titanite"),
        DS3LocationData("LC: Large Soul of a Nameless Soldier - dark room mid",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("LC: Ember - plaza center", "Ember"),
        DS3LocationData("LC: Winged Knight Helm - ascent, behind illusory wall",
                        "Winged Knight Helm", hidden=True),
        DS3LocationData("LC: Winged Knight Armor - ascent, behind illusory wall",
                        "Winged Knight Armor", hidden=True),
        DS3LocationData("LC: Winged Knight Gauntlets - ascent, behind illusory wall",
                        "Winged Knight Gauntlets", hidden=True),
        DS3LocationData("LC: Winged Knight Leggings - ascent, behind illusory wall",
                        "Winged Knight Leggings", hidden=True),
        DS3LocationData("LC: Rusted Coin - chapel", "Rusted Coin x2"),
        DS3LocationData("LC: Braille Divine Tome of Lothric - wyvern room",
                        "Braille Divine Tome of Lothric", hidden=True),  # Hidden fall
        DS3LocationData("LC: Red Tearstone Ring - chapel, drop onto roof", "Red Tearstone Ring"),
        DS3LocationData("LC: Twinkling Titanite - moat, left side", "Twinkling Titanite x2"),
        DS3LocationData("LC: Large Soul of a Nameless Soldier - plaza left, by pillar",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("LC: Titanite Scale - altar", "Titanite Scale x3"),
        DS3LocationData("LC: Titanite Scale - chapel, chest", "Titanite Scale"),
        DS3LocationData("LC: Hood of Prayer", "Hood of Prayer"),
        DS3LocationData("LC: Robe of Prayer - ascent, chest at beginning", "Robe of Prayer"),
        DS3LocationData("LC: Skirt of Prayer - ascent, chest at beginning", "Skirt of Prayer"),
        DS3LocationData("LC: Spirit Tree Crest Shield - basement, chest",
                        "Spirit Tree Crest Shield"),
        DS3LocationData("LC: Titanite Scale - basement, chest", "Titanite Scale"),
        DS3LocationData("LC: Twinkling Titanite - basement, chest #1", "Twinkling Titanite"),
        DS3LocationData("LC: Twinkling Titanite - basement, chest #2", "Twinkling Titanite x2"),
        DS3LocationData("LC: Life Ring+2 - dark room mid, out door opposite wyvern, drop down",
                        "Life Ring+2", ngp=True, hidden=True),  # Hidden fall
        DS3LocationData("LC: Dark Stoneplate Ring+1 - wyvern room, balcony",
                        "Dark Stoneplate Ring+1", ngp=True, hidden=True),  # Hidden fall
        DS3LocationData("LC: Thunder Stoneplate Ring+2 - chapel, drop onto roof",
                        "Thunder Stoneplate Ring+2", ngp=True),
        DS3LocationData("LC: Sunlight Straight Sword - wyvern room, mimic",
                        "Sunlight Straight Sword", mimic=True, hidden=True),  # Hidden fall
        DS3LocationData("LC: Titanite Scale - dark room, upper, mimic", "Titanite Scale x3",
                        mimic=True),
        DS3LocationData("LC: Ember - wyvern room, wyvern foot mob drop", "Ember x2",
                        drop=True, hidden=True),  # Hidden fall, Pus of Man Wyvern drop
        DS3LocationData("LC: Titanite Chunk - wyvern room, wyvern foot mob drop", "Titanite Chunk x2",
                        drop=True, hidden=True),  # Hidden fall, Pus of Man Wyvern drop
        DS3LocationData("LC: Ember - dark room mid, pus of man mob drop", "Ember x2",
                        drop=True),  # Pus of Man Wyvern drop
        DS3LocationData("LC: Titanite Chunk - dark room mid, pus of man mob drop",
                        "Titanite Chunk x2"),
        DS3LocationData("LC: Irithyll Rapier - basement, miniboss drop", "Irithyll Rapier",
                        miniboss=True),  # Boreal Outrider drop
        DS3LocationData("LC: Twinkling Titanite - dark room mid, out door opposite wyvern, lizard",
                        "Twinkling Titanite x2", lizard=True, missable=True),
        DS3LocationData("LC: Twinkling Titanite - moat, right path, lizard",
                        "Twinkling Titanite x2", lizard=True, missable=True),
        DS3LocationData("LC: Gotthard Twinswords - by Grand Archives door, after PC and AL bosses",
                        "Gotthard Twinswords", conditional=True),
        DS3LocationData("LC: Grand Archives Key - by Grand Archives door, after PC and AL bosses",
                        "Grand Archives Key", prominent=True, progression=True,
                        conditional=True),
        DS3LocationData("LC: Titanite Chunk - down stairs after boss", "Titanite Chunk"),

        # Eygon of Carim (kill or quest)
        DS3LocationData("FS: Morne's Great Hammer - Eygon", "Morne's Great Hammer", npc=True),
        DS3LocationData("FS: Moaning Shield - Eygon", "Moaning Shield", npc=True),

        # Shrine Handmaid after killing Dragonslayer Armour (or Eygon of Carim)
        DS3LocationData("FS: Dancer's Crown - shop after killing LC entry boss", "Dancer's Crown",
                        boss=True, shop=True),
        DS3LocationData("FS: Dancer's Armor - shop after killing LC entry boss", "Dancer's Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Dancer's Gauntlets - shop after killing LC entry boss",
                        "Dancer's Gauntlets", boss=True, shop=True),
        DS3LocationData("FS: Dancer's Leggings - shop after killing LC entry boss",
                        "Dancer's Leggings", boss=True, shop=True),

        # Shrine Handmaid after killing Dragonslayer Armour (or Eygon of Carim)
        DS3LocationData("FS: Morne's Helm - shop after killing Eygon or LC boss", "Morne's Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Morne's Armor - shop after killing Eygon or LC boss", "Morne's Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Morne's Gauntlets - shop after killing Eygon or LC boss",
                        "Morne's Gauntlets", boss=True, shop=True),
        DS3LocationData("FS: Morne's Leggings - shop after killing Eygon or LC boss",
                        "Morne's Leggings", boss=True, shop=True),
    ],
    "Consumed King's Garden": [
        DS3LocationData("CKG: Soul of Consumed Oceiros", "Soul of Consumed Oceiros",
                        prominent=True, boss=True),
        # Could classify this as "hidden" because it's midway down an elevator, but the elevator is
        # so slow and the midway point is so obvious that it's not actually hard to find.
        DS3LocationData("CKG: Estus Shard - balcony", "Estus Shard"),
        DS3LocationData("CKG: Shadow Mask - under center platform", "Shadow Mask"),
        DS3LocationData("CKG: Shadow Garb - under rotunda", "Shadow Garb"),
        DS3LocationData("CKG: Shadow Gauntlets - under rotunda", "Shadow Gauntlets"),
        DS3LocationData("CKG: Shadow Leggings - under rotunda", "Shadow Leggings"),
        DS3LocationData("CKG: Black Firebomb - under rotunda", "Black Firebomb x2"),
        DS3LocationData("CKG: Claw - under rotunda", "Claw"),
        DS3LocationData("CKG: Titanite Chunk - up lone stairway", "Titanite Chunk"),
        DS3LocationData("CKG: Dragonscale Ring - shortcut, leave halfway down lift",
                        "Dragonscale Ring"),
        DS3LocationData("CKG: Human Pine Resin - toxic pool, past rotunda", "Human Pine Resin"),
        DS3LocationData("CKG: Titanite Chunk - shortcut", "Titanite Chunk"),
        DS3LocationData("CKG: Titanite Chunk - balcony, drop onto rubble", "Titanite Chunk"),
        DS3LocationData("CKG: Soul of a Weary Warrior - before first lift",
                        "Soul of a Weary Warrior"),
        DS3LocationData("CKG: Dark Gem - under lone stairway", "Dark Gem"),
        DS3LocationData("CKG: Titanite Scale - shortcut", "Titanite Scale"),
        DS3LocationData("CKG: Human Pine Resin - pool by lift", "Human Pine Resin x2"),
        DS3LocationData("CKG: Titanite Chunk - right of shortcut lift bottom", "Titanite Chunk"),
        DS3LocationData("CKG: Ring of Sacrifice - under balcony", "Ring of Sacrifice"),
        DS3LocationData("CKG: Wood Grain Ring+1 - by first elevator bottom", "Wood Grain Ring+1",
                        ngp=True),
        DS3LocationData("CKG: Sage Ring+2 - balcony, drop onto rubble, jump back", "Sage Ring+2",
                        ngp=True, hidden=True),
        DS3LocationData("CKG: Titanite Scale - tomb, chest #1", "Titanite Scale"),
        DS3LocationData("CKG: Titanite Scale - tomb, chest #2", "Titanite Scale"),
        DS3LocationData("CKG: Magic Stoneplate Ring - mob drop before boss",
                        "Magic Stoneplate Ring", drop=True,
                        hidden=True),  # Guaranteed drop from a normal-looking Cathedral Knight

        # After Oceiros's boss room, only once the Drakeblood summon in AP has been killed
        DS3LocationData("CKG: Drakeblood Helm - tomb, after killing AP mausoleum NPC",
                        "Drakeblood Helm", hostile_npc=True, hidden=True),
        DS3LocationData("CKG: Drakeblood Armor - tomb, after killing AP mausoleum NPC",
                        "Drakeblood Armor", hostile_npc=True, hidden=True),
        DS3LocationData("CKG: Drakeblood Gauntlets - tomb, after killing AP mausoleum NPC",
                        "Drakeblood Gauntlets", hostile_npc=True, hidden=True),
        DS3LocationData("CKG: Drakeblood Leggings - tomb, after killing AP mausoleum NPC",
                        "Drakeblood Leggings", hostile_npc=True, hidden=True),
    ],
    "Grand Archives": [
        DS3LocationData("GA: Titanite Slab - final elevator secret", "Titanite Slab",
                        hidden=True),
        DS3LocationData("GA: Soul of the Twin Princes", "Soul of the Twin Princes", boss=True),
        DS3LocationData("GA: Cinders of a Lord - Lothric Prince",
                        "Cinders of a Lord - Lothric Prince",
                        static="09,0:50002040::", prominent=True, progression=True,
                        boss=True),
        DS3LocationData("GA: Onikiri and Ubadachi - outside 5F, NPC drop", "Onikiri and Ubadachi",
                        hostile_npc=True,  # Black Hand Kamui drop
                        missable=True),  # This is placed at the location the NPC gets randomized
        # to, which makes it hard to include in logic.
        DS3LocationData("GA: Golden Wing Crest Shield - outside 5F, NPC drop",
                        "Golden Wing Crest Shield",
                        hostile_npc=True),  # Lion Knight Albert drop
        DS3LocationData("GA: Sage's Crystal Staff - outside 5F, NPC drop",
                        "Sage's Crystal Staff",
                        hostile_npc=True),  # Daughter of Crystal Kriemhild drop
        DS3LocationData("GA: Titanite Chunk - 1F, up right stairs", "Titanite Chunk"),
        DS3LocationData("GA: Titanite Chunk - 1F, path from wax pool", "Titanite Chunk"),
        DS3LocationData("GA: Soul of a Crestfallen Knight - 1F, loop left after drop",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("GA: Titanite Chunk - 1F, balcony", "Titanite Chunk"),
        DS3LocationData("GA: Fleshbite Ring - up stairs from 4F", "Fleshbite Ring"),
        DS3LocationData("GA: Soul of a Crestfallen Knight - path to dome",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("GA: Soul of a Nameless Soldier - dark room", "Soul of a Nameless Soldier"),
        DS3LocationData("GA: Crystal Chime - 1F, path from wax pool", "Crystal Chime"),
        DS3LocationData("GA: Titanite Scale - dark room, upstairs", "Titanite Scale"),
        DS3LocationData("GA: Estus Shard - dome, far balcony", "Estus Shard"),
        DS3LocationData("GA: Homeward Bone - 2F early balcony", "Homeward Bone x3"),
        DS3LocationData("GA: Titanite Scale - 2F, titanite scale atop bookshelf", "Titanite Scale",
                        hidden=True),  # Hidden fall
        DS3LocationData("GA: Titanite Chunk - 2F, by wax pool", "Titanite Chunk"),
        DS3LocationData("GA: Hollow Gem - rooftops lower, in hall", "Hollow Gem",
                        hidden=True),  # Hidden fall
        DS3LocationData("GA: Titanite Scale - 3F, corner up stairs", "Titanite Scale"),
        DS3LocationData("GA: Titanite Scale - 1F, up stairs on bookshelf", "Titanite Scale"),
        DS3LocationData("GA: Titanite Scale - 3F, by ladder to 2F late", "Titanite Scale",
                        hidden=True),  # Hidden by a table
        DS3LocationData("GA: Shriving Stone - 2F late, by ladder from 3F", "Shriving Stone"),
        DS3LocationData("GA: Large Soul of a Crestfallen Knight - 4F, back",
                        "Large Soul of a Crestfallen Knight"),
        DS3LocationData("GA: Titanite Chunk - rooftops, balcony", "Titanite Chunk"),
        DS3LocationData("GA: Titanite Scale - rooftops lower, path to 2F", "Titanite Scale x3",
                        hidden=True),  # Hidden fall
        DS3LocationData("GA: Titanite Chunk - rooftops lower, ledge by buttress", "Titanite Chunk",
                        hidden=True),  # Hidden fall
        DS3LocationData("GA: Soul of a Weary Warrior - rooftops, by lizards",
                        "Soul of a Weary Warrior"),
        DS3LocationData("GA: Titanite Chunk - rooftops, just before 5F", "Titanite Chunk"),
        DS3LocationData("GA: Ember - 5F, by entrance", "Ember"),
        DS3LocationData("GA: Blessed Gem - rafters", "Blessed Gem"),
        DS3LocationData("GA: Titanite Chunk - 5F, far balcony", "Titanite Chunk x2"),
        DS3LocationData("GA: Large Soul of a Crestfallen Knight - outside 5F",
                        "Large Soul of a Crestfallen Knight"),
        DS3LocationData("GA: Avelyn - 1F, drop from 3F onto bookshelves", "Avelyn",
                        hidden=True),  # Hidden fall
        DS3LocationData("GA: Titanite Chunk - 2F, right after dark room", "Titanite Chunk"),
        DS3LocationData("GA: Hunter's Ring - dome, very top", "Hunter's Ring"),
        DS3LocationData("GA: Divine Pillars of Light - cage above rafters",
                        "Divine Pillars of Light"),
        DS3LocationData("GA: Power Within - dark room, behind retractable bookshelf",
                        "Power Within", hidden=True),  # Switch in darkened room
        DS3LocationData("GA: Sage Ring+1 - rafters, second level down", "Sage Ring+1", ngp=True),
        DS3LocationData("GA: Lingering Dragoncrest Ring+2 - dome, room behind spire",
                        "Lingering Dragoncrest Ring+2", ngp=True),
        DS3LocationData("GA: Divine Blessing - rafters, down lower level ladder",
                        "Divine Blessing"),
        DS3LocationData("GA: Twinkling Titanite - rafters, down lower level ladder",
                        "Twinkling Titanite x3"),
        DS3LocationData("GA: Witch's Locks - dark room, behind retractable bookshelf",
                        "Witch's Locks", hidden=True),  # Switch in darkened room
        DS3LocationData("GA: Titanite Slab - 1F, after pulling 2F switch", "Titanite Slab",
                        hidden=True),
        DS3LocationData("GA: Titanite Scale - 4F, chest by exit", "Titanite Scale x3"),
        DS3LocationData("GA: Soul Stream - 3F, behind illusory wall", "Soul Stream",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("GA: Scholar Ring - 2F, between late and early", "Scholar Ring"),
        DS3LocationData("GA: Undead Bone Shard - 5F, by entrance", "Undead Bone Shard"),
        DS3LocationData("GA: Titanite Slab - dome, kill all mobs", "Titanite Slab",
                        drop=True,
                        hidden=True),  # Guaranteed drop from killing all Winged Knights
        DS3LocationData("GA: Outrider Knight Helm - 3F, behind illusory wall, miniboss drop",
                        "Outrider Knight Helm", miniboss=True,
                        hidden=True),  # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Armor - 3F, behind illusory wall, miniboss drop",
                        "Outrider Knight Armor", miniboss=True,
                        hidden=True),  # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Gauntlets - 3F, behind illusory wall, miniboss drop",
                        "Outrider Knight Gauntlets", miniboss=True,
                        hidden=True),  # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Outrider Knight Leggings - 3F, behind illusory wall, miniboss drop",
                        "Outrider Knight Leggings", miniboss=True,
                        hidden=True),  # Behind illusory wall, Outrider Knight drop
        DS3LocationData("GA: Crystal Scroll - 2F late, miniboss drop", "Crystal Scroll",
                        miniboss=True),  # Crystal Sage drop
        DS3LocationData("GA: Twinkling Titanite - dark room, lizard #1", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("GA: Chaos Gem - dark room, lizard", "Chaos Gem", lizard=True),
        DS3LocationData("GA: Twinkling Titanite - 1F, lizard by drop", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("GA: Crystal Gem - 1F, lizard by drop", "Crystal Gem", lizard=True),
        DS3LocationData("GA: Twinkling Titanite - 2F, lizard by entrance", "Twinkling Titanite x2",
                        lizard=True),
        DS3LocationData("GA: Titanite Scale - 1F, drop from 2F late onto bookshelves, lizard",
                        "Titanite Scale x2", lizard=True, hidden=True),  # Hidden fall
        DS3LocationData("GA: Twinkling Titanite - rooftops, lizard #1", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("GA: Heavy Gem - rooftops, lizard", "Heavy Gem", lizard=True),
        DS3LocationData("GA: Twinkling Titanite - rooftops, lizard #2", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("GA: Sharp Gem - rooftops, lizard", "Sharp Gem", lizard=True),
        DS3LocationData("GA: Twinkling Titanite - up stairs from 4F, lizard", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("GA: Refined Gem - up stairs from 4F, lizard", "Refined Gem",
                        lizard=True),
        DS3LocationData("GA: Twinkling Titanite - dark room, lizard #2", "Twinkling Titanite x2",
                        lizard=True),

        # Shrine Handmaid after killing NPCs
        DS3LocationData("FS: Faraam Helm - shop after killing GA NPC", "Faraam Helm",
                        hidden=True, hostile_npc=True, shop=True),
        DS3LocationData("FS: Faraam Armor - shop after killing GA NPC", "Faraam Armor",
                        hidden=True, hostile_npc=True, shop=True),
        DS3LocationData("FS: Faraam Gauntlets - shop after killing GA NPC", "Faraam Gauntlets",
                        hidden=True, hostile_npc=True, shop=True),
        DS3LocationData("FS: Faraam Boots - shop after killing GA NPC", "Faraam Boots",
                        hidden=True, hostile_npc=True, shop=True),
        DS3LocationData("FS: Black Hand Hat - shop after killing GA NPC", "Black Hand Hat",
                        hidden=True, hostile_npc=True, shop=True),
        DS3LocationData("FS: Black Hand Armor - shop after killing GA NPC", "Black Hand Armor",
                        hidden=True, hostile_npc=True, shop=True),

        # Shrine Handmaid after killing Lothric, Younger Prince
        DS3LocationData("FS: Lorian's Helm - shop after killing GA boss", "Lorian's Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Lorian's Armor - shop after killing GA boss", "Lorian's Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Lorian's Gauntlets - shop after killing GA boss", "Lorian's Gauntlets",
                        boss=True, shop=True),
        DS3LocationData("FS: Lorian's Leggings - shop after killing GA boss", "Lorian's Leggings",
                        boss=True, shop=True),

        # Sirris quest completion + beat Twin Princes
        DS3LocationData("FS: Sunless Talisman - Sirris, kill GA boss", "Sunless Talisman",
                        missable=True, npc=True),
        DS3LocationData("FS: Sunless Veil - shop, Sirris quest, kill GA boss", "Sunless Veil",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Sunless Armor - shop, Sirris quest, kill GA boss", "Sunless Armor",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Sunless Gauntlets - shop, Sirris quest, kill GA boss",
                        "Sunless Gauntlets", missable=True, npc=True, shop=True),
        DS3LocationData("FS: Sunless Leggings - shop, Sirris quest, kill GA boss",
                        "Sunless Leggings", missable=True, npc=True, shop=True),

        # Unbreakable Patches
        DS3LocationData("FS: Hidden Blessing - Patches after searching GA", "Hidden Blessing",
                        missable=True, npc=True, shop=True),
    ],
    "Untended Graves": [
        DS3LocationData("UG: Soul of Champion Gundyr", "Soul of Champion Gundyr", prominent=True,
                        boss=True),
        DS3LocationData("UG: Priestess Ring - shop", "Priestess Ring", shop=True),
        DS3LocationData("UG: Shriving Stone - swamp, by bonfire", "Shriving Stone"),
        DS3LocationData("UG: Titanite Chunk - swamp, left path by fountain", "Titanite Chunk"),
        DS3LocationData("UG: Soul of a Crestfallen Knight - swamp, center",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("UG: Titanite Chunk - swamp, right path by fountain", "Titanite Chunk"),
        DS3LocationData("UG: Ashen Estus Ring - swamp, path opposite bonfire", "Ashen Estus Ring"),
        DS3LocationData("UG: Black Knight Glaive - boss arena", "Black Knight Glaive"),
        DS3LocationData("UG: Hidden Blessing - cemetery, behind coffin", "Hidden Blessing"),
        DS3LocationData("UG: Eyes of a Fire Keeper - shrine, Irina's room", "Eyes of a Fire Keeper",
                        hidden=True),  # Illusory wall
        DS3LocationData("UG: Soul of a Crestfallen Knight - environs, above shrine entrance",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("UG: Blacksmith Hammer - shrine, Andre's room", "Blacksmith Hammer"),
        DS3LocationData("UG: Chaos Blade - environs, left of shrine", "Chaos Blade"),
        DS3LocationData("UG: Hornet Ring - environs, right of main path after killing FK boss",
                        "Hornet Ring", conditional=True),
        DS3LocationData("UG: Coiled Sword Fragment - shrine, dead bonfire", "Coiled Sword Fragment",
                        boss=True),
        DS3LocationData("UG: Life Ring+3 - shrine, behind big throne", "Life Ring+3", ngp=True),
        DS3LocationData("UG: Ring of Steel Protection+1 - environs, behind bell tower",
                        "Ring of Steel Protection+1", ngp=True),

        # Yuria shop, or Shrine Handmaiden with Hollow's Ashes
        # This is here because this is where the ashes end up if you kill Yoel or Yuria
        DS3LocationData("FS: Ring of Sacrifice - Yuria shop", "Ring of Sacrifice",
                        static='99,0:-1:40000,110000,70000107,70000116:', npc=True,
                        shop=True),

        # Untended Graves Handmaid
        # All shop items are missable because she can be killed, except Priestess ring because she
        # drops it on death anyway.
        DS3LocationData("UG: Ember - shop", "Ember", shop=True, missable=True),
        # Untended Graves Handmaid after killing Abyss Watchers
        DS3LocationData("UG: Wolf Knight Helm - shop after killing FK boss", "Wolf Knight Helm",
                        boss=True, shop=True, conditional=True,
                        missable=True),
        DS3LocationData("UG: Wolf Knight Armor - shop after killing FK boss",
                        "Wolf Knight Armor", boss=True, shop=True, missable=True),
        DS3LocationData("UG: Wolf Knight Gauntlets - shop after killing FK boss",
                        "Wolf Knight Gauntlets", boss=True, shop=True, missable=True),
        DS3LocationData("UG: Wolf Knight Leggings - shop after killing FK boss",
                        "Wolf Knight Leggings", boss=True, shop=True, missable=True),

        # Shrine Handmaid after killing Champion Gundyr
        DS3LocationData("FS: Gundyr's Helm - shop after killing UG boss", "Gundyr's Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Gundyr's Armor - shop after killing UG boss", "Gundyr's Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Gundyr's Gauntlets - shop after killing UG boss", "Gundyr's Gauntlets",
                        boss=True, shop=True),
        DS3LocationData("FS: Gundyr's Leggings - shop after killing UG boss", "Gundyr's Leggings",
                        boss=True, shop=True),
    ],
    "Archdragon Peak": [
        DS3LocationData("AP: Dragon Head Stone - fort, boss drop", "Dragon Head Stone",
                        prominent=True, boss=True),
        DS3LocationData("AP: Soul of the Nameless King", "Soul of the Nameless King",
                        prominent=True, boss=True),
        DS3LocationData("AP: Dragon Tooth - belfry roof, NPC drop", "Dragon Tooth",
                        hostile_npc=True),  # Havel Knight drop
        DS3LocationData("AP: Havel's Greatshield - belfry roof, NPC drop", "Havel's Greatshield",
                        hostile_npc=True),  # Havel Knight drop
        DS3LocationData("AP: Drakeblood Greatsword - mausoleum, NPC drop", "Drakeblood Greatsword",
                        hostile_npc=True),
        DS3LocationData("AP: Ricard's Rapier - belfry, NPC drop", "Ricard's Rapier",
                        hostile_npc=True),
        DS3LocationData("AP: Lightning Clutch Ring - intro, left of boss door",
                        "Lightning Clutch Ring"),
        DS3LocationData("AP: Stalk Dung Pie - fort overlook", "Stalk Dung Pie x6"),
        DS3LocationData("AP: Titanite Chunk - fort, second room balcony", "Titanite Chunk"),
        DS3LocationData("AP: Titanite Scale - mausoleum, downstairs balcony #1",
                        "Titanite Scale"),
        DS3LocationData("AP: Soul of a Weary Warrior - intro, first cliff edge",
                        "Soul of a Weary Warrior"),
        DS3LocationData("AP: Titanite Chunk - intro, left before archway", "Titanite Chunk"),
        DS3LocationData("AP: Lightning Gem - intro, side rise", "Lightning Gem"),
        DS3LocationData("AP: Homeward Bone - intro, path to bonfire", "Homeward Bone x2"),
        DS3LocationData("AP: Soul of a Nameless Soldier - intro, right before archway",
                        "Soul of a Nameless Soldier"),
        DS3LocationData("AP: Titanite Chunk - intro, archway corner", "Titanite Chunk"),
        DS3LocationData("AP: Ember - fort overlook #1", "Ember"),
        DS3LocationData("AP: Large Soul of a Weary Warrior - fort, center",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("AP: Large Soul of a Nameless Soldier - fort, by stairs to first room",
                        "Large Soul of a Nameless Soldier"),
        DS3LocationData("AP: Lightning Urn - fort, left of first room entrance",
                        "Lightning Urn x4"),
        DS3LocationData("AP: Lightning Bolt - rotunda", "Lightning Bolt x12"),
        DS3LocationData("AP: Titanite Chunk - rotunda", "Titanite Chunk x2"),
        # Not 100% sure about this location name, can't find this on any maps
        DS3LocationData("AP: Dung Pie - fort, landing after second room", "Dung Pie x3"),
        DS3LocationData("AP: Titanite Scale - mausoleum, downstairs balcony #2", "Titanite Scale"),
        DS3LocationData("AP: Soul of a Weary Warrior - walkway, building window",
                        "Soul of a Weary Warrior"),
        DS3LocationData("AP: Soul of a Crestfallen Knight - mausoleum, upstairs",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("AP: Titanite Chunk - intro, behind rock", "Titanite Chunk"),
        DS3LocationData("AP: Ember - fort overlook #2", "Ember"),
        DS3LocationData("AP: Thunder Stoneplate Ring - walkway, up ladder",
                        "Thunder Stoneplate Ring"),
        DS3LocationData("AP: Titanite Scale - mausoleum, upstairs balcony", "Titanite Scale"),
        DS3LocationData("AP: Ember - belfry, below bell", "Ember"),
        DS3LocationData("AP: Ancient Dragon Greatshield - intro, on archway",
                        "Ancient Dragon Greatshield"),
        DS3LocationData("AP: Large Soul of a Crestfallen Knight - summit, by fountain",
                        "Large Soul of a Crestfallen Knight"),
        DS3LocationData("AP: Dragon Chaser's Ashes - summit, side path", "Dragon Chaser's Ashes",
                        progression=True),
        DS3LocationData("AP: Ember - intro, by bonfire", "Ember"),
        DS3LocationData("AP: Dragonslayer Spear - gate after mausoleum", "Dragonslayer Spear"),
        DS3LocationData("AP: Dragonslayer Helm - plaza", "Dragonslayer Helm"),
        DS3LocationData("AP: Dragonslayer Armor - plaza", "Dragonslayer Armor"),
        DS3LocationData("AP: Dragonslayer Gauntlets - plaza", "Dragonslayer Gauntlets"),
        DS3LocationData("AP: Dragonslayer Leggings - plaza", "Dragonslayer Leggings"),
        DS3LocationData("AP: Twinkling Titanite - fort, end of rafters", "Twinkling Titanite x2"),
        DS3LocationData("AP: Twinkling Titanite - fort, down second room balcony ladder",
                        "Twinkling Titanite x2"),
        DS3LocationData("AP: Titanite Slab - belfry roof", "Titanite Slab"),
        DS3LocationData("AP: Great Magic Barrier - drop off belfry roof", "Great Magic Barrier",
                        hidden=True),  # Hidden fall
        DS3LocationData("AP: Titanite Slab - plaza", "Titanite Slab"),
        DS3LocationData("AP: Ring of Steel Protection - fort overlook, beside stairs",
                        "Ring of Steel Protection"),
        DS3LocationData("AP: Havel's Ring+1 - summit, after building", "Havel's Ring+1",
                        ngp=True),
        DS3LocationData("AP: Covetous Gold Serpent Ring+2 - plaza", "Covetous Gold Serpent Ring+2",
                        ngp=True),
        DS3LocationData("AP: Titanite Scale - walkway building", "Titanite Scale x3"),
        DS3LocationData("AP: Twinkling Titanite - belfry, by ladder to roof",
                        "Twinkling Titanite x3"),
        DS3LocationData("AP: Twinkling Dragon Torso Stone - summit, gesture at altar",
                        "Twinkling Dragon Torso Stone", hidden=True),  # Requires gesture
        DS3LocationData("AP: Calamity Ring - mausoleum, gesture at altar", "Calamity Ring",
                        hidden=True),  # Requires gesture
        DS3LocationData("AP: Twinkling Titanite - walkway building, lizard",
                        "Twinkling Titanite x3", lizard=True),
        DS3LocationData("AP: Titanite Chunk - walkway, miniboss drop", "Titanite Chunk x6",
                        miniboss=True),  # Wyvern miniboss drop
        DS3LocationData("AP: Titanite Scale - walkway, miniboss drop", "Titanite Scale x3",
                        miniboss=True),  # Wyvern miniboss drop
        DS3LocationData("AP: Twinkling Titanite - walkway, miniboss drop", "Twinkling Titanite x3",
                        miniboss=True),  # Wyvern miniboss drop
        DS3LocationData("FS: Hawkwood's Swordgrass - Andre after gesture in AP summit",
                        "Hawkwood's Swordgrass", conditional=True, hidden=True),

        # Shrine Handmaid after killing Nameless King
        DS3LocationData("FS: Golden Crown - shop after killing AP boss", "Golden Crown",
                        boss=True, shop=True),
        DS3LocationData("FS: Dragonscale Armor - shop after killing AP boss", "Dragonscale Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Golden Bracelets - shop after killing AP boss", "Golden Bracelets",
                        boss=True, shop=True),
        DS3LocationData("FS: Dragonscale Waistcloth - shop after killing AP boss",
                        "Dragonscale Waistcloth", boss=True, shop=True),
        DS3LocationData("FK: Twinkling Dragon Head Stone - Hawkwood drop",
                        "Twinkling Dragon Head Stone", missable=True,
                        npc=True),  # Hawkwood (quest)
    ],
    "Kiln of the First Flame": [
        DS3LocationData("KFF: Soul of the Lords", "Soul of the Lords", boss=True),

        # Shrine Handmaid after placing all Cinders of a Lord
        DS3LocationData("FS: Titanite Slab - shop after placing all Cinders", "Titanite Slab",
                        static='99,0:-1:9210,110000:', hidden=True),
        DS3LocationData("FS: Firelink Helm - shop after placing all Cinders", "Firelink Helm",
                        boss=True, shop=True),
        DS3LocationData("FS: Firelink Armor - shop after placing all Cinders", "Firelink Armor",
                        boss=True, shop=True),
        DS3LocationData("FS: Firelink Gauntlets - shop after placing all Cinders",
                        "Firelink Gauntlets", boss=True, shop=True),
        DS3LocationData("FS: Firelink Leggings - shop after placing all Cinders",
                        "Firelink Leggings", boss=True, shop=True),

        # Yuria (quest, after Soul of Cinder)
        DS3LocationData("FS: Billed Mask - shop after killing Yuria", "Billed Mask",
                        missable=True, npc=True),
        DS3LocationData("FS: Black Dress - shop after killing Yuria", "Black Dress",
                        missable=True, npc=True),
        DS3LocationData("FS: Black Gauntlets - shop after killing Yuria", "Black Gauntlets",
                        missable=True, npc=True),
        DS3LocationData("FS: Black Leggings - shop after killing Yuria", "Black Leggings",
                        missable=True, npc=True),
    ],

    # DLC
    "Painted World of Ariandel (Before Contraption)": [
        DS3LocationData("PW1: Valorheart - boss drop", "Valorheart", prominent=True, boss=True),
        DS3LocationData("PW1: Contraption Key - library, NPC drop", "Contraption Key",
                        prominent=True, progression=True,
                        hostile_npc=True),  # Sir Vilhelm drop
        DS3LocationData("PW1: Onyx Blade - library, NPC drop", "Onyx Blade",
                        hostile_npc=True),  # Sir Vilhelm drop
        DS3LocationData("PW1: Chillbite Ring - Friede", "Chillbite Ring",
                        npc=True),  # Friede conversation
        DS3LocationData("PW1: Rime-blue Moss Clump - snowfield upper, starting cave",
                        "Rime-blue Moss Clump x2"),
        DS3LocationData("PW1: Poison Gem - snowfield upper, forward from bonfire", "Poison Gem"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - snowfield lower, path back up",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Follower Javelin - snowfield lower, path back up", "Follower Javelin"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - snowfield lower, path to village",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Homeward Bone - snowfield village, outcropping", "Homeward Bone x6"),
        DS3LocationData("PW1: Blessed Gem - snowfield, behind tower", "Blessed Gem",
                        hidden=True),  # Hidden behind a tower
        DS3LocationData("PW1: Captain's Ashes - snowfield tower, 6F", "Captain's Ashes",
                        progression=True),
        DS3LocationData("PW1: Black Firebomb - snowfield lower, path to bonfire",
                        "Black Firebomb x2"),
        DS3LocationData("PW1: Shriving Stone - below bridge near", "Shriving Stone"),
        DS3LocationData("PW1: Millwood Greatarrow - snowfield village, loop back to lower",
                        "Millwood Greatarrow x5"),
        DS3LocationData("PW1: Millwood Greatbow - snowfield village, loop back to lower",
                        "Millwood Greatbow"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - snowfield upper",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Rusted Coin - snowfield lower, straight from fall", "Rusted Coin"),
        DS3LocationData("PW1: Large Titanite Shard - snowfield lower, left from fall",
                        "Large Titanite Shard"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - settlement courtyard, cliff",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Crow Quills - settlement loop, jump into courtyard", "Crow Quills",
                        hidden=True),  # Hidden fall
        DS3LocationData("PW1: Simple Gem - settlement, lowest level, behind gate", "Simple Gem"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - settlement, by ladder to bonfire",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Slave Knight Hood - settlement roofs, drop by ladder",
                        "Slave Knight Hood"),
        DS3LocationData("PW1: Slave Knight Armor - settlement roofs, drop by ladder",
                        "Slave Knight Armor"),
        DS3LocationData("PW1: Slave Knight Gauntlets - settlement roofs, drop by ladder",
                        "Slave Knight Gauntlets"),
        DS3LocationData("PW1: Slave Knight Leggings - settlement roofs, drop by ladder",
                        "Slave Knight Leggings"),
        DS3LocationData("PW1: Ember - settlement main, left building after bridge", "Ember"),
        DS3LocationData("PW1: Dark Gem - settlement back, egg building", "Dark Gem"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - settlement roofs, balcony",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - settlement loop, by bonfire",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Rusted Gold Coin - settlement roofs, roof near second ladder",
                        "Rusted Gold Coin x3"),
        DS3LocationData("PW1: Soul of a Crestfallen Knight - settlement hall, rafters",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("PW1: Way of White Corona - settlement hall, by altar",
                        "Way of White Corona"),
        DS3LocationData("PW1: Rusted Coin - right of library", "Rusted Coin x2"),
        DS3LocationData("PW1: Young White Branch - right of library", "Young White Branch"),
        DS3LocationData("PW1: Budding Green Blossom - settlement courtyard, ledge",
                        "Budding Green Blossom x3"),
        DS3LocationData("PW1: Crow Talons - settlement roofs, near bonfire", "Crow Talons"),
        DS3LocationData("PW1: Hollow Gem - beside chapel", "Hollow Gem"),
        DS3LocationData("PW1: Rime-blue Moss Clump - below bridge far", "Rime-blue Moss Clump x4"),
        DS3LocationData("PW1: Follower Sabre - roots above depths", "Follower Sabre"),
        DS3LocationData("PW1: Ember - roots above depths", "Ember"),
        DS3LocationData("PW1: Snap Freeze - depths, far end, mob drop", "Snap Freeze", drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Tree Woman
        DS3LocationData("PW1: Rime-blue Moss Clump - snowfield upper, overhang",
                        "Rime-blue Moss Clump"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - snowfield lower, by cliff",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Ember - settlement, building near bonfire", "Ember"),
        DS3LocationData("PW1: Frozen Weapon - snowfield lower, egg zone", "Frozen Weapon"),
        DS3LocationData("PW1: Titanite Slab - depths, up secret ladder", "Titanite Slab",
                        static='11,0:54500640::',
                        hidden=True),  # Must kill normal-looking Tree Woman
        DS3LocationData("PW1: Homeward Bone - depths, up hill", "Homeward Bone x2"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - below snowfield village overhang",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Large Soul of a Weary Warrior - settlement hall roof",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("PW1: Large Soul of an Unknown Traveler - settlement back",
                        "Large Soul of an Unknown Traveler"),
        DS3LocationData("PW1: Heavy Gem - snowfield village", "Heavy Gem"),
        DS3LocationData("PW1: Large Soul of a Weary Warrior - snowfield tower, 6F",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("PW1: Millwood Battle Axe - snowfield tower, 5F", "Millwood Battle Axe"),
        DS3LocationData("PW1: Ethereal Oak Shield - snowfield tower, 3F", "Ethereal Oak Shield"),
        DS3LocationData("PW1: Soul of a Weary Warrior - snowfield tower, 1F",
                        "Soul of a Weary Warrior"),
        DS3LocationData("PW1: Twinkling Titanite - snowfield tower, 3F lizard",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("PW1: Large Titanite Shard - lizard under bridge near",
                        "Large Titanite Shard", lizard=True),
        DS3LocationData("PW1: Twinkling Titanite - roots, lizard", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("PW1: Twinkling Titanite - settlement roofs, lizard before hall",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("PW1: Large Titanite Shard - settlement loop, lizard",
                        "Large Titanite Shard x2", lizard=True),
    ],
    "Painted World of Ariandel (After Contraption)": [
        DS3LocationData("PW2: Soul of Sister Friede", "Soul of Sister Friede", prominent=True,
                        boss=True),
        DS3LocationData("PW2: Titanite Slab - boss drop", "Titanite Slab",
                        static='11,0:50004700::',
                        boss=True),  # One-time drop after Friede Phase 2
        DS3LocationData("PW2: Floating Chaos - NPC drop", "Floating Chaos", hostile_npc=True,
                        hidden=True),  # Livid Pyromancer Dunnel drop (requires ember)
        DS3LocationData("PW2: Prism Stone - pass, tree by beginning", "Prism Stone x10"),
        DS3LocationData("PW2: Titanite Chunk - pass, cliff overlooking bonfire", "Titanite Chunk"),
        DS3LocationData("PW2: Titanite Chunk - pass, by kickable tree", "Titanite Chunk"),
        DS3LocationData("PW2: Follower Shield - pass, far cliffside", "Follower Shield"),
        DS3LocationData("PW2: Large Titanite Shard - pass, just before B1",
                        "Large Titanite Shard x2"),
        DS3LocationData("PW2: Quakestone Hammer - pass, side path near B1", "Quakestone Hammer"),
        DS3LocationData("PW2: Ember - pass, central alcove", "Ember"),
        DS3LocationData("PW2: Large Titanite Shard - pass, far side path",
                        "Large Titanite Shard x2"),
        DS3LocationData("PW2: Soul of a Crestfallen Knight - pit edge #1",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("PW2: Soul of a Crestfallen Knight - pit edge #2",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("PW2: Large Soul of a Crestfallen Knight - pit, by tree",
                        "Large Soul of a Crestfallen Knight"),
        DS3LocationData("PW2: Earth Seeker - pit cave", "Earth Seeker"),
        DS3LocationData("PW2: Follower Torch - pass, far side path", "Follower Torch"),
        DS3LocationData("PW2: Dung Pie - B1", "Dung Pie x2"),
        DS3LocationData("PW2: Vilhelm's Helm", "Vilhelm's Helm"),
        DS3LocationData("PW2: Vilhelm's Armor - B2, along wall", "Vilhelm's Armor"),
        DS3LocationData("PW2: Vilhelm's Gauntlets - B2, along wall", "Vilhelm's Gauntlets"),
        DS3LocationData("PW2: Vilhelm's Leggings - B2, along wall", "Vilhelm's Leggings"),
        DS3LocationData("PW2: Blood Gem - B2, center", "Blood Gem"),
        DS3LocationData("PW2: Pyromancer's Parting Flame - rotunda",
                        "Pyromancer's Parting Flame", hidden=True),  # Behind illusory wall
        DS3LocationData("PW2: Homeward Bone - rotunda", "Homeward Bone x2",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("PW2: Twinkling Titanite - B3, lizard #1", "Twinkling Titanite",
                        lizard=True),
        DS3LocationData("PW2: Twinkling Titanite - B3, lizard #2", "Twinkling Titanite",
                        lizard=True),

        # Corvian Settler after killing Friede
        DS3LocationData("PW1: Titanite Slab - Corvian", "Titanite Slab", npc=True),

        # Shrine Handmaid after killing Sister Friede
        DS3LocationData("FS: Ordained Hood - shop after killing PW2 boss", "Ordained Hood",
                        boss=True, shop=True),
        DS3LocationData("FS: Ordained Dress - shop after killing PW2 boss", "Ordained Dress",
                        boss=True, shop=True),
        DS3LocationData("FS: Ordained Trousers - shop after killing PW2 boss", "Ordained Trousers",
                        boss=True, shop=True),
    ],
    "Dreg Heap": [
        DS3LocationData("DH: Soul of the Demon Prince", "Soul of the Demon Prince",
                        prominent=True, boss=True),
        DS3LocationData("DH: Siegbräu - Lapp", "Siegbräu", missable=True, drop=True,
                        npc=True),  # Lapp (quest or kill)
        DS3LocationData("DH: Flame Fan - swamp upper, NPC drop", "Flame Fan",
                        hostile_npc=True),  # Desert Pyromancer Zoey drop
        DS3LocationData("DH: Ember - castle, behind spire", "Ember"),
        DS3LocationData("DH: Soul of a Weary Warrior - castle overhang", "Soul of a Weary Warrior"),
        DS3LocationData("DH: Titanite Chunk - castle, up stairs", "Titanite Chunk"),
        DS3LocationData("DH: Aquamarine Dagger - castle, up stairs", "Aquamarine Dagger"),
        DS3LocationData("DH: Twinkling Titanite - library, chandelier", "Twinkling Titanite"),
        DS3LocationData("DH: Murky Hand Scythe - library, behind bookshelves", "Murky Hand Scythe"),
        DS3LocationData("DH: Divine Blessing - library, after drop", "Divine Blessing"),
        DS3LocationData("DH: Ring of Steel Protection+3 - ledge before church",
                        "Ring of Steel Protection+3"),
        DS3LocationData("DH: Soul of a Crestfallen Knight - church, altar",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("DH: Rusted Coin - behind fountain after church", "Rusted Coin x2"),
        DS3LocationData("DH: Titanite Chunk - pantry, first room", "Titanite Chunk"),
        DS3LocationData("DH: Murky Longstaff - pantry, last room", "Murky Longstaff"),
        DS3LocationData("DH: Ember - pantry, behind crates just before upstairs", "Ember",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("DH: Great Soul Dregs - pantry upstairs", "Great Soul Dregs",
                        hidden=True),  # Behind illusory wall
        DS3LocationData("DH: Covetous Silver Serpent Ring+3 - pantry upstairs, drop down",
                        "Covetous Silver Serpent Ring+3", hidden=True),  # Behind illusory wall
        DS3LocationData("DH: Titanite Chunk - path from church, by pillar", "Titanite Chunk"),
        DS3LocationData("DH: Homeward Bone - end of path from church", "Homeward Bone x3"),
        DS3LocationData("DH: Lightning Urn - wall outside church", "Lightning Urn x4"),
        DS3LocationData("DH: Projected Heal - parapets balcony", "Projected Heal"),
        DS3LocationData("DH: Large Soul of a Weary Warrior - parapets, hall",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("DH: Lothric War Banner - parapets, end of hall", "Lothric War Banner"),
        DS3LocationData("DH: Titanite Scale - library, back of room", "Titanite Scale"),
        DS3LocationData("DH: Black Firebomb - ruins, up windmill from bonfire", "Black Firebomb x4"),
        DS3LocationData("DH: Titanite Chunk - ruins, path from bonfire", "Titanite Chunk"),
        DS3LocationData("DH: Twinkling Titanite - ruins, root near bonfire", "Twinkling Titanite"),
        DS3LocationData("DH: Desert Pyromancer Garb - ruins, by shack near cliff",
                        "Desert Pyromancer Garb"),
        DS3LocationData("DH: Titanite Chunk - ruins, by far shack", "Titanite Chunk x2"),
        DS3LocationData("DH: Giant Door Shield - ruins, path below far shack", "Giant Door Shield"),
        DS3LocationData("DH: Ember - ruins, alcove before swamp", "Ember"),
        DS3LocationData("DH: Desert Pyromancer Gloves - swamp, far right",
                        "Desert Pyromancer Gloves"),
        DS3LocationData("DH: Desert Pyromancer Skirt - swamp right, by roots",
                        "Desert Pyromancer Skirt"),
        DS3LocationData("DH: Titanite Scale - swamp upper, drop and jump into tower",
                        "Titanite Scale"),
        DS3LocationData("DH: Purple Moss Clump - swamp shack", "Purple Moss Clump x4"),
        DS3LocationData("DH: Ring of Favor+3 - swamp right, up root", "Ring of Favor+3"),
        DS3LocationData("DH: Titanite Chunk - swamp right, drop partway up root", "Titanite Chunk"),
        DS3LocationData("DH: Large Soul of a Weary Warrior - swamp, under overhang",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("DH: Titanite Slab - swamp, path under overhang", "Titanite Slab"),
        DS3LocationData("DH: Titanite Chunk - swamp, along buildings", "Titanite Chunk"),
        DS3LocationData("DH: Loincloth - swamp, left edge", "Loincloth"),
        DS3LocationData("DH: Titanite Chunk - swamp, path to upper", "Titanite Chunk"),
        DS3LocationData("DH: Large Soul of a Weary Warrior - swamp center",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("DH: Harald Curved Greatsword - swamp left, under root",
                        "Harald Curved Greatsword"),
        DS3LocationData("DH: Homeward Bone - swamp left, on root", "Homeward Bone"),
        DS3LocationData("DH: Prism Stone - swamp upper, tunnel start", "Prism Stone x6"),
        DS3LocationData("DH: Desert Pyromancer Hood - swamp upper, tunnel end",
                        "Desert Pyromancer Hood"),
        DS3LocationData("DH: Twinkling Titanite - swamp upper, drop onto root",
                        "Twinkling Titanite", hidden=True),  # Hidden fall
        DS3LocationData("DH: Divine Blessing - swamp upper, building roof", "Divine Blessing"),
        DS3LocationData("DH: Ember - ruins, alcove on cliff", "Ember", hidden=True),  # Hidden fall
        DS3LocationData("DH: Small Envoy Banner - boss drop", "Small Envoy Banner",
                        progression=True, boss=True),
        DS3LocationData("DH: Twinkling Titanite - ruins, alcove on cliff, mob drop",
                        "Twinkling Titanite x2", drop=True,
                        hidden=True),  # Hidden fall, also guaranteed drop from killing normal-looking pilgrim
        DS3LocationData("DH: Twinkling Titanite - swamp upper, mob drop on roof",
                        "Twinkling Titanite x2", drop=True,
                        hidden=True),  # Hidden fall, also guaranteed drop from killing normal-looking pilgrim
        DS3LocationData("DH: Twinkling Titanite - path after church, mob drop",
                        "Twinkling Titanite x2", drop=True,
                        hidden=True),  # Guaranteed drop from killing normal-looking pilgrim

        # Stone-humped Hag's shop
        DS3LocationData("DH: Splitleaf Greatsword - shop", "Splitleaf Greatsword", shop=True),
        DS3LocationData("DH: Divine Blessing - shop", "Divine Blessing", shop=True),
        DS3LocationData("DH: Hidden Blessing - shop", "Hidden Blessing", shop=True),
        DS3LocationData("DH: Rusted Gold Coin - shop", "Rusted Gold Coin", shop=True),
        DS3LocationData("DH: Ember - shop", "Ember", shop=True),
    ],
    "Ringed City": [
        DS3LocationData("RC: Titanite Slab - mid boss drop", "Titanite Slab",
                        prominent=True, boss=True),  # Halflight drop, only once
        DS3LocationData("RC: Filianore's Spear Ornament - mid boss drop",
                        "Filianore's Spear Ornament"),
        DS3LocationData("RC: Soul of Darkeater Midir", "Soul of Darkeater Midir", prominent=True,
                        boss=True),
        DS3LocationData("RC: Sacred Chime of Filianore - ashes, NPC drop",
                        "Sacred Chime of Filianore",
                        hostile_npc=True),  # Shira (kill or quest)
        DS3LocationData("RC: Titanite Slab - ashes, NPC drop", "Titanite Slab",
                        hostile_npc=True),  # Shira (kill or quest)
        DS3LocationData("RC: Crucifix of the Mad King - ashes, NPC drop",
                        "Crucifix of the Mad King", hostile_npc=True),  # Shira drop
        DS3LocationData("RC: Ledo's Great Hammer - streets high, opposite building, NPC drop",
                        "Ledo's Great Hammer", hostile_npc=True,
                        missable=True),  # Silver Knight Ledo drop, doesn't invade once Halflight
        # is defeated
        DS3LocationData("RC: Wolf Ring+3 - street gardens, NPC drop", "Wolf Ring+3",
                        hostile_npc=True,
                        missable=True),  # Alva drop, doesn't invade once Halflight is defeated
        DS3LocationData("RC: Blindfold Mask - grave, NPC drop", "Blindfold Mask",
                        hostile_npc=True),  # Moaning Knight drop
        DS3LocationData("RC: Titanite Scale - wall top, behind spawn", "Titanite Scale"),  # wrong
        DS3LocationData("RC: Ruin Helm - wall top, under stairs to bonfire", "Ruin Helm"),
        DS3LocationData("RC: Ruin Armor - wall top, under stairs to bonfire", "Ruin Armor"),
        DS3LocationData("RC: Ruin Gauntlets - wall top, under stairs to bonfire", "Ruin Gauntlets"),
        DS3LocationData("RC: Ruin Leggings - wall top, under stairs to bonfire", "Ruin Leggings"),
        DS3LocationData("RC: Budding Green Blossom - wall top, in flower cluster",
                        "Budding Green Blossom x2"),
        DS3LocationData("RC: Titanite Chunk - wall top, among graves", "Titanite Chunk x2"),
        DS3LocationData("RC: Ember - wall top, by statue", "Ember"),
        DS3LocationData("RC: Budding Green Blossom - wall top, flowers by stairs",
                        "Budding Green Blossom x2"),
        DS3LocationData("RC: Hidden Blessing - wall top, tomb under platform", "Hidden Blessing",
                        hidden=True),  # hidden fall
        DS3LocationData("RC: Soul of a Crestfallen Knight - wall top, under drop",
                        "Soul of a Crestfallen Knight", hidden=True),  # hidden fall
        DS3LocationData("RC: Large Soul of a Weary Warrior - wall top, right of small tomb",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("RC: Ember - wall upper, balcony", "Ember"),
        DS3LocationData("RC: Purging Stone - wall top, by door to upper", "Purging Stone x2"),
        DS3LocationData("RC: Hollow Gem - wall upper, path to tower", "Hollow Gem"),
        DS3LocationData("RC: Titanite Chunk - wall upper, courtyard alcove", "Titanite Chunk"),
        DS3LocationData("RC: Twinkling Titanite - wall tower, jump from chandelier",
                        "Twinkling Titanite", hidden=True),  # Hidden fall
        DS3LocationData("RC: Shriving Stone - wall tower, bottom floor center", "Shriving Stone"),
        DS3LocationData("RC: Shira's Crown - Shira's room after killing ashes NPC", "Shira's Crown",
                        hidden=True),  # Have to return to a cleared area
        DS3LocationData("RC: Shira's Armor - Shira's room after killing ashes NPC", "Shira's Armor",
                        hidden=True),  # Have to return to a cleared area
        DS3LocationData("RC: Shira's Gloves - Shira's room after killing ashes NPC",
                        "Shira's Gloves", hidden=True),  # Have to return to a cleared area
        DS3LocationData("RC: Shira's Trousers - Shira's room after killing ashes NPC",
                        "Shira's Trousers", hidden=True),  # Have to return to a cleared area
        DS3LocationData("RC: Mossfruit - streets near left, path to garden", "Mossfruit x2"),
        DS3LocationData("RC: Large Soul of a Crestfallen Knight - streets, far stairs",
                        "Large Soul of a Crestfallen Knight"),
        DS3LocationData("RC: Ringed Knight Spear - streets, down far right hall",
                        "Ringed Knight Spear"),
        DS3LocationData("RC: Black Witch Hat - streets garden", "Black Witch Hat",
                        hostile_npc=True),  # Alva
        DS3LocationData("RC: Black Witch Garb - streets garden", "Black Witch Garb",
                        hostile_npc=True),  # Alva
        DS3LocationData("RC: Black Witch Wrappings - streets garden", "Black Witch Wrappings",
                        hostile_npc=True),  # Alva
        DS3LocationData("RC: Black Witch Trousers - streets garden", "Black Witch Trousers",
                        hostile_npc=True),  # Alva
        DS3LocationData("RC: Dragonhead Shield - streets monument, across bridge",
                        "Dragonhead Shield", hidden=True),  # "Show Your Humanity" puzzle
        DS3LocationData("RC: Titanite Chunk - streets, near left drop", "Titanite Chunk",
                        hidden=True),  # Hidden fall
        DS3LocationData("RC: Mossfruit - streets, far left alcove", "Mossfruit x2"),
        DS3LocationData("RC: Large Soul of a Crestfallen Knight - streets monument, across bridge",
                        "Large Soul of a Crestfallen Knight",
                        hidden=True),  # "Show Your Humanity" puzzle
        DS3LocationData("RC: Covetous Gold Serpent Ring+3 - streets, by Lapp",
                        "Covetous Gold Serpent Ring+3"),
        DS3LocationData("RC: Titanite Chunk - streets high, building opposite", "Titanite Chunk x2"),
        DS3LocationData("RC: Dark Gem - swamp near, by stairs", "Dark Gem"),
        DS3LocationData("RC: Prism Stone - swamp near, railing by bonfire", "Prism Stone x4"),
        DS3LocationData("RC: Ringed Knight Straight Sword - swamp near, tower on peninsula",
                        "Ringed Knight Straight Sword"),
        DS3LocationData("RC: Havel's Ring+3 - streets high, drop from building opposite",
                        "Havel's Ring+3", hidden=True),  # Hidden fall
        DS3LocationData("RC: Titanite Chunk - swamp near left, by spire top", "Titanite Chunk"),
        DS3LocationData("RC: Twinkling Titanite - swamp near left", "Twinkling Titanite"),
        DS3LocationData("RC: Soul of a Weary Warrior - swamp center", "Soul of a Weary Warrior"),
        DS3LocationData("RC: Preacher's Right Arm - swamp near right, by tower",
                        "Preacher's Right Arm"),
        DS3LocationData("RC: Rubbish - swamp far, by crystal", "Rubbish"),
        DS3LocationData("RC: Titanite Chunk - swamp near right, behind rock",
                        "Titanite Chunk"),
        DS3LocationData("RC: Black Witch Veil - swamp near right, by sunken church",
                        "Black Witch Veil"),
        DS3LocationData("RC: Twinkling Titanite - swamp near right, on sunken church",
                        "Twinkling Titanite"),
        DS3LocationData("RC: Soul of a Crestfallen Knight - swamp near left, nook",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("RC: White Preacher Head - swamp near, nook right of stairs",
                        "White Preacher Head"),
        DS3LocationData("RC: Titanite Scale - swamp far, by miniboss", "Titanite Scale"),
        DS3LocationData("RC: Dragonhead Greatshield - lower cliff, under bridge",
                        "Dragonhead Greatshield"),
        DS3LocationData("RC: Titanite Scale - lower cliff, path under bridge", "Titanite Scale x2"),
        DS3LocationData("RC: Rubbish - lower cliff, middle", "Rubbish"),
        DS3LocationData("RC: Large Soul of a Weary Warrior - lower cliff, end",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("RC: Titanite Scale - lower cliff, first alcove", "Titanite Scale x2"),
        DS3LocationData("RC: Titanite Scale - lower cliff, lower path", "Titanite Scale"),
        DS3LocationData("RC: Lightning Gem - grave, room after first drop", "Lightning Gem"),
        DS3LocationData("RC: Blessed Gem - grave, down lowest stairs", "Blessed Gem"),
        DS3LocationData("RC: Simple Gem - grave, up stairs after first drop", "Simple Gem"),
        DS3LocationData("RC: Large Soul of a Weary Warrior - wall lower, past two illusory walls",
                        "Large Soul of a Weary Warrior", hidden=True),
        DS3LocationData("RC: Lightning Arrow - wall lower, past three illusory walls",
                        "Lightning Arrow"),
        DS3LocationData("RC: Chloranthy Ring+3 - wall hidden, drop onto statue",
                        "Chloranthy Ring+3", hidden=True),  # Hidden fall
        DS3LocationData("RC: Ember - wall hidden, statue room", "Ember"),
        DS3LocationData("RC: Filianore's Spear Ornament - wall hidden, by ladder",
                        "Filianore's Spear Ornament"),
        DS3LocationData("RC: Antiquated Plain Garb - wall hidden, before boss",
                        "Antiquated Plain Garb"),
        DS3LocationData("RC: Violet Wrappings - wall hidden, before boss", "Violet Wrappings"),
        DS3LocationData("RC: Soul of a Weary Warrior - lower cliff, by first alcove",
                        "Soul of a Weary Warrior"),
        DS3LocationData("RC: Twinkling Titanite - church path, left of boss door",
                        "Twinkling Titanite x2"),
        DS3LocationData("RC: Budding Green Blossom - church path", "Budding Green Blossom x3"),
        DS3LocationData("RC: Titanite Chunk - swamp center, peninsula edge", "Titanite Chunk"),
        DS3LocationData("RC: Large Soul of a Weary Warrior - swamp center, by peninsula",
                        "Large Soul of a Weary Warrior"),
        DS3LocationData("RC: Soul of a Weary Warrior - swamp right, by sunken church",
                        "Soul of a Weary Warrior"),
        DS3LocationData("RC: Titanite Scale - upper cliff, bridge", "Titanite Scale"),
        DS3LocationData("RC: Soul of a Crestfallen Knight - swamp far, behind crystal",
                        "Soul of a Crestfallen Knight"),
        DS3LocationData("RC: White Birch Bow - swamp far left, up hill", "White Birch Bow"),
        DS3LocationData("RC: Titanite Chunk - swamp far left, up hill", "Titanite Chunk"),
        DS3LocationData("RC: Young White Branch - swamp far left, by white tree #1",
                        "Young White Branch"),
        DS3LocationData("RC: Young White Branch - swamp far left, by white tree #2",
                        "Young White Branch"),
        DS3LocationData("RC: Young White Branch - swamp far left, by white tree #3",
                        "Young White Branch"),
        DS3LocationData("RC: Ringed Knight Paired Greatswords - church path, mob drop",
                        "Ringed Knight Paired Greatswords", drop=True,
                        hidden=True),  # Guaranteed drop from a normal-looking Ringed Knight
        DS3LocationData("RC: Hidden Blessing - swamp center, mob drop", "Hidden Blessing",
                        drop=True, hidden=True),  # Guaranteed drop from Judicator
        DS3LocationData("RC: Divine Blessing - wall top, mob drop", "Divine Blessing",
                        drop=True, hidden=True),  # Guaranteed drop from Judicator
        DS3LocationData("RC: Divine Blessing - streets monument, mob drop", "Divine Blessing",
                        drop=True,
                        hidden=True),  # Guaranteed drop from Judicator, "Show Your Humanity" puzzle
        DS3LocationData("RC: Ring of the Evil Eye+3 - grave, mimic", "Ring of the Evil Eye+3",
                        mimic=True),
        DS3LocationData("RC: Iron Dragonslayer Helm - swamp far, miniboss drop",
                        "Iron Dragonslayer Helm", miniboss=True),
        DS3LocationData("RC: Iron Dragonslayer Armor - swamp far, miniboss drop",
                        "Iron Dragonslayer Armor", miniboss=True),
        DS3LocationData("RC: Iron Dragonslayer Gauntlets - swamp far, miniboss drop",
                        "Iron Dragonslayer Gauntlets", miniboss=True),
        DS3LocationData("RC: Iron Dragonslayer Leggings - swamp far, miniboss drop",
                        "Iron Dragonslayer Leggings", miniboss=True),
        DS3LocationData("RC: Church Guardian Shiv - swamp far left, in building",
                        "Church Guardian Shiv"),
        DS3LocationData("RC: Spears of the Church - hidden boss drop", "Spears of the Church",
                        boss=True),  # Midir drop
        DS3LocationData("RC: Ritual Spear Fragment - church path", "Ritual Spear Fragment"),
        DS3LocationData("RC: Titanite Scale - swamp far, lagoon entrance", "Titanite Scale"),
        DS3LocationData("RC: Twinkling Titanite - grave, lizard past first drop",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("RC: Titanite Scale - grave, lizard past first drop", "Titanite Scale",
                        lizard=True),
        DS3LocationData("RC: Twinkling Titanite - streets high, lizard", "Twinkling Titanite x2",
                        lizard=True),
        DS3LocationData("RC: Titanite Scale - wall lower, lizard", "Titanite Scale", lizard=True),
        DS3LocationData("RC: Twinkling Titanite - wall top, lizard on side path",
                        "Twinkling Titanite", lizard=True),
        DS3LocationData("RC: Soul of Slave Knight Gael", "Soul of Slave Knight Gael",
                        prominent=True, boss=True),
        DS3LocationData("RC: Blood of the Dark Soul - end boss drop", "Blood of the Dark Soul"),
        DS3LocationData("RC: Titanite Slab - ashes, mob drop", "Titanite Slab",
                        drop=True,
                        hidden=True),  # Guaranteed drop from normal-looking Ringed Knight

        # Lapp
        DS3LocationData("RC: Siegbräu - Lapp", "Siegbräu", missable=True,
                        npc=True),  # Lapp (quest)
        # Quest or Shrine Handmaiden after death
        DS3LocationData("RC: Lapp's Helm - Lapp", "Lapp's Helm", npc=True, shop=True),
        DS3LocationData("RC: Lapp's Armor - Lapp", "Lapp's Armor", npc=True, shop=True),
        DS3LocationData("RC: Lapp's Gauntlets - Lapp", "Lapp's Gauntlets", npc=True, shop=True),
        DS3LocationData("RC: Lapp's Leggings - Lapp", "Lapp's Leggings", npc=True, shop=True),
    ],

    # Unlockable shops. We only bother creating a "region" for these for shops that are locked
    # behind keys and always have items available either through the shop or through the NPC's
    # ashes.
    "Greirat's Shop": [
        DS3LocationData("FS: Blue Tearstone Ring - Greirat", "Blue Tearstone Ring",
                        static='01,0:50006120::', npc=True),
        DS3LocationData("FS: Ember - Greirat", "Ember", static="99,0:-1:110000,120000,70000110:",
                        shop=True, npc=True),

        # Undead Settlement rewards
        DS3LocationData("FS: Divine Blessing - Greirat from US", "Divine Blessing",
                        static='99,0:-1:110000,120000,70000150,70000175:', missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Ember - Greirat from US", "Ember",
                        static='99,0:-1:110000,120000,70000150,70000175:', missable=True,
                        shop=True, npc=True),

        # Irityhll rewards
        DS3LocationData("FS: Divine Blessing - Greirat from IBV", "Divine Blessing",
                        static='99,0:-1:110000,120000,70000151,70000176:', missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Hidden Blessing - Greirat from IBV", "Hidden Blessing",
                        static='99,0:-1:110000,120000,70000151,70000176:', missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Titanite Scale - Greirat from IBV", "Titanite Scale",
                        static='99,0:-1:110000,120000,70000151,70000176:', missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Twinkling Titanite - Greirat from IBV", "Twinkling Titanite",
                        static='99,0:-1:110000,120000,70000151,70000176:', missable=True,
                        shop=True, npc=True),

        # Lothric rewards (from Shrine Handmaid)
        DS3LocationData("FS: Ember - shop for Greirat's Ashes", "Twinkling Titanite",
                        static='99,0:-1:110000,120000,70000152,70000177:', missable=True,
                        shop=True, npc=True),
    ],
    "Karla's Shop": [
        DS3LocationData("FS: Affinity - Karla", "Affinity", shop=True, npc=True),
        DS3LocationData("FS: Dark Edge - Karla", "Dark Edge", shop=True, npc=True),

        # Quelana Pyromancy Tome
        DS3LocationData("FS: Firestorm - Karla for Quelana Tome", "Firestorm", missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Rapport - Karla for Quelana Tome", "Rapport", missable=True,
                        shop=True, npc=True),
        DS3LocationData("FS: Fire Whip - Karla for Quelana Tome", "Fire Whip", missable=True,
                        shop=True, npc=True),

        # Grave Warden Pyromancy Tome
        DS3LocationData("FS: Black Flame - Karla for Grave Warden Tome", "Black Flame",
                        missable=True, shop=True, npc=True),
        DS3LocationData("FS: Black Fire Orb - Karla for Grave Warden Tome", "Black Fire Orb",
                        missable=True, shop=True, npc=True),

        # Deep Braille Divine Tome. This can also be given to Irina, but it'll fail her quest
        DS3LocationData("FS: Gnaw - Karla for Deep Braille Tome", "Gnaw", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Deep Protection - Karla for Deep Braille Tome", "Deep Protection",
                        missable=True, npc=True, shop=True),

        # Londor Braille Divine Tome. This can also be given to Irina, but it'll fail her quest
        DS3LocationData("FS: Vow of Silence - Karla for Londor Tome", "Vow of Silence",
                        missable=True, npc=True, shop=True),
        DS3LocationData("FS: Dark Blade - Karla for Londor Tome", "Dark Blade", missable=True,
                        npc=True, shop=True),
        DS3LocationData("FS: Dead Again - Karla for Londor Tome", "Dead Again", missable=True,
                        npc=True, shop=True),

        # Drops on death. Missable because the player would have to decide between killing her or
        # seeing everything she sells.
        DS3LocationData("FS: Karla's Pointed Hat - kill Karla", "Karla's Pointed Hat",
                        static='07,0:50006150::', missable=True, drop=True, npc=True),
        DS3LocationData("FS: Karla's Coat - kill Karla", "Karla's Coat",
                        static='07,0:50006150::', missable=True, drop=True, npc=True),
        DS3LocationData("FS: Karla's Gloves - kill Karla", "Karla's Gloves",
                        static='07,0:50006150::', missable=True, drop=True, npc=True),
        DS3LocationData("FS: Karla's Trousers - kill Karla", "Karla's Trousers",
                        static='07,0:50006150::', missable=True, drop=True, npc=True),
    ],
}

for i, region in enumerate(region_order):
    for location in location_tables[region]: location.region_value = i

for region in [
    "Painted World of Ariandel (Before Contraption)",
    "Painted World of Ariandel (After Contraption)",
    "Dreg Heap",
    "Ringed City",
]:
    for location in location_tables[region]:
        location.dlc = True

for region in [
    "Firelink Shrine Bell Tower",
    "Greirat's Shop",
    "Karla's Shop"
]:
    for location in location_tables[region]:
        location.conditional = True

location_name_groups: Dict[str, Set[str]] = {
    # We could insert these locations automatically with setdefault(), but we set them up explicitly
    # instead so we can choose the ordering.
    "Prominent": set(),
    "Progression": set(),
    "Boss Rewards": set(),
    "Miniboss Rewards": set(),
    "Mimic Rewards": set(),
    "Hostile NPC Rewards": set(),
    "Friendly NPC Rewards": set(),
    "Small Crystal Lizards": set(),
    "Upgrade": set(),
    "Small Souls": set(),
    "Boss Souls": set(),
    "Unique": set(),
    "Healing": set(),
    "Miscellaneous": set(),
    "Hidden": set(),
    "Weapons": set(),
    "Shields": set(),
    "Armor": set(),
    "Rings": set(),
    "Spells": set(),
}

location_descriptions = {
    "Prominent": "A small number of locations that are in very obvious locations. Mostly boss " + \
                 "drops. Ideal for setting as priority locations.",
    "Progression": "Locations that contain items in vanilla which unlock other locations.",
    "Boss Rewards": "Boss drops. Does not include soul transfusions or shop items.",
    "Miniboss Rewards": "Miniboss drops. Only includes enemies considered minibosses by the " + \
                        "enemy randomizer.",
    "Mimic Rewards": "Drops from enemies that are mimics in vanilla.",
    "Hostile NPC Rewards": "Drops from NPCs that are hostile to you. This includes scripted " + \
                           "invaders and initially-friendly NPCs that must be fought as part of their quest.",
    "Friendly NPC Rewards": "Items given by friendly NPCs as part of their quests or from " + \
                            "non-violent interaction.",
    "Upgrade": "Locations that contain upgrade items in vanilla, including titanite, gems, and " + \
               "Shriving Stones.",
    "Small Souls": "Locations that contain soul items in vanilla, not including boss souls.",
    "Boss Souls": "Locations that contain boss souls in vanilla, as well as Soul of Rosaria.",
    "Unique": "Locations that contain items in vanilla that are unique per NG cycle, such as " + \
              "scrolls, keys, ashes, and so on. Doesn't cover equipment, spells, or souls.",
    "Healing": "Locations that contain Undead Bone Shards and Estus Shards in vanilla.",
    "Miscellaneous": "Locations that contain generic stackable items in vanilla, such as arrows, " +
                     "firebombs, buffs, and so on.",
    "Hidden": "Locations that are particularly difficult to find, such as behind illusory " + \
              "walls, down hidden drops, and so on. Does not include large locations like Untended " + \
              "Graves or Archdragon Peak.",
    "Weapons": "Locations that contain weapons in vanilla.",
    "Shields": "Locations that contain shields in vanilla.",
    "Armor": "Locations that contain armor in vanilla.",
    "Rings": "Locations that contain rings in vanilla.",
    "Spells": "Locations that contain spells in vanilla.",
}

location_dictionary: Dict[str, DS3LocationData] = {}
for location_name, location_table in location_tables.items():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})

    for location_data in location_table:
        if not location_data.is_event:
            for group_name in location_data.location_groups():
                location_name_groups[group_name].add(location_data.name)

    # Allow entire locations to be added to location sets.
    if not location_name.endswith(" Shop"):
        location_name_groups[location_name] = set([
            location_data.name for location_data in location_table
            if not location_data.is_event
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
