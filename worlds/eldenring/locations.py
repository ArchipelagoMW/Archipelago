from typing import cast, ClassVar, Optional, Dict, List, Set
from dataclasses import dataclass

from BaseClasses import ItemClassification, Location, Region
from .items import ERItemCategory, item_table

# Regions in approximate order of progression
#MARK: Location Order
region_order = [
    "Chapel of Anticipation",

    #Limgrave
    "Stranded Graveyard",
    "Fringefolk Hero's Grave",
    "Limgrave",
    "Church of Elleh",
    "Coastal Cave",
    "Church of Dragon Communion",
    "Groveside Cave",
    "Stormfoot Catacombs",
    "Gatefront Ruins",
    "Limgrave Tunnels",
    "Stormgate",
    "Stormhill Shack",
    "Waypoint Ruins",
    "Dragon-Burnt Ruins",
    "Murkwater Cave",
    "Mistwood Ruins",
    "Fort Haight",
    "Third Church of Marika",
    "LG Artist's Shack",
    "Summonwater Village",
    "Murkwater Catacombs",
    "Highroad Cave",
    "Deathtouched Catacombs",





    # Weeping

    # Liurnia
    "Liurnia of The Lakes",

    # Caelid
    "Caelid",
    "Smoldering Church",
]
"""

    "Roundtable Hold",
    "Siofra River",
    "Stormveil Castle",

    #Weeping
    "Weeping Peninsula",
    "Castle Morne",

    #Liurnia
    "Raya Lucaria Academy",
    "Chapel of Anticipation [Return]",
    "Caria Manor",
    "Ainsel River",
    "Lake of Rot",

    #Caelid
    "Dragonbarrow",
    "Redmane Castle",
    "Nokron, Eternal City",
    "Deeproot Depths",
    #Altus
    "Ruin-Strewn Precipice",
    "Altus Plateau",
    "The Shaded Castle",
    "Mt.Gelmir",
    "Volcano Manor",
    "Capital Outskirts",
    #Leyndell
    "Leyndell, Royal Capital",
    "Subterranean Shunning-Grounds",
    #Mountain
    "Forbidden Lands",
    "Mountaintops of The Giants", 
    "Castle Sol",
    #Farum Azula
    "Crumbling Farum Azula",
    "Leyndell, Ashen Capital",
    #Snowfield
    "Consecrated Snowfield", 
    "Mohgwyn Palace",
    "Miquellas Haligtree",
]"""

#MARK: DLC Location Order
region_order_dlc = [
    #DLC
    "Gravesite Plain",
]
    
"""    
    "Scadu Altus",
    "Rauh Base",
    "Ancient Ruins of Rauh",
    "Cerulean Coast",
    "Charo's Hidden Grave",
    "Jagged Peak",
    "Abyssal Woods",
    "Finger Ruins of Rhia",
    "Scaduview",
]"""

@dataclass
class ERLocationData:
    __location_id: ClassVar[int] = 7000000
    """The next location ID to use when creating location data."""

    name: str
    """The name of this location according to Archipelago.

    This needs to be unique within this world."""

    default_item_name: Optional[str]
    """The name of the item that appears by default in this location.

    If this is None, that indicates that this location is an "event" that's
    automatically considered accessed as soon as it's available. Events are used
    to indicate major game transitions that aren't otherwise gated by items so
    that progression balancing and item smoothing is more accurate for ER.
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

    mainboss: bool = False
    """Whether this location is a reward for defeating a main boss."""

    boss: bool = False
    """Whether this location is a reward for defeating a boss."""

    drop: bool = False
    """Whether this is an item dropped by a (non-boss) enemy.

    This is automatically set to True if scarab, is True.
    """

    hostile_npc: bool = False
    """Whether this location is dropped by a hostile NPC."""

    shop: bool = False
    """Whether this location can appear in an NPC's shop."""

    conditional: bool = False
    """Whether this location is conditional on a progression item.

    This is used to track locations that won't become available until an unknown amount of time into
    the run, and as such shouldn't have "similar to the base game" items placed in them.
    """

    hidden: bool = False
    """Whether this location is particularly tricky to find.

    This is for players without an encyclopedic knowledge of ER who don't want to get stuck looking
    for an illusory wall or one random mob with a guaranteed drop.
    """

    scarab: bool = False
    """Whether this location is dropped by a scarab."""



    @property
    def is_event(self) -> bool:
        """Whether this location represents an event rather than a specific item pickup."""
        return self.default_item_name is None

    def __post_init__(self):
        if not self.is_event:
            self.ap_code = self.ap_code or ERLocationData.__location_id
            ERLocationData.__location_id += 1
        if self.scarab or self.hostile_npc: self.drop = True

    def location_groups(self) -> List[str]:
        """The names of location groups this location should appear in.

        This is computed from the properties assigned to this location."""
        names = []
        if self.prominent: names.append("Prominent")
        if self.progression: names.append("Progression")
        if self.mainboss: names.append("Main Boss Rewards")
        if self.boss: names.append("Boss Rewards")
        if self.hostile_npc: names.append("Hostile NPC Rewards")
        if self.npc: names.append("Friendly NPC Rewards")

        default_item = item_table[cast(str, self.default_item_name)]
        names.append({
                         ERItemCategory.GOODS: "Goods",
                         ERItemCategory.WEAPON: "Weapons",
                         ERItemCategory.ARMOR: "Armor",
                         ERItemCategory.ACCESSORY: "Accessory",
                         ERItemCategory.ASHOFWAR: "Ash of war",
                         ERItemCategory.CUSTOMWEAPON: "Upgraded Weapons",
                     }[default_item.category])
        if default_item.classification == ItemClassification.progression:
            names.append("Progression")

        return names


class ERLocation(Location):
    game: str = "EldenRing"
    data: ERLocationData

    def __init__(
            self,
            player: int,
            data: ERLocationData,
            parent: Optional[Region] = None,
            event: bool = False):
        super().__init__(player, data.name, None if event else data.ap_code, parent)
        self.data = data

# from ds3 locations.py

# * Avoid using vanilla enemy placements as landmarks, because these are
#   randomized by the enemizer by default. Instead, use generic terms like
#   "mob", "boss", and "miniboss".

# * Location descriptions don't need to direct the player to the precise spot.
#   You can assume the player is broadly familiar with Eldenring or willing
#   to look at a vanilla guide. Just give a general area to look in or an idea
#   of what quest a check is connected to. Terseness is valuable: try to keep
#   each location description short enough that the whole line doesn't exceed
#   100 characters.

# * Use "[name] drop" for items that require killing an NPC who becomes hostile
#   as part of their normal quest, "kill [name]" for items that require killing
#   them even when they aren't hostile, and just "[name]" for items that are
#   naturally available as part of their quest.

# for descriptions 
# [area acronym]/[grace or location acronym]: [original item] - [what gives item, if it does] [direction from grace] or [very brief description]

# CD/AFCHN: Lifesteal Fist - scarab to NW         # grace
# LG/WR: Golden Rune [1] - graveyard S of WR      # location
# LG/(CE): Smithing Stone [1] - on anvil          # within location

# for shops with inf of an item, leave to be nothing

# ERLocationData(":  - ", ""),
#MARK: Locations
location_tables: Dict[str, List[ERLocationData]] = {
    "Chapel of Anticipation":[
        ERLocationData("CA: Ornamental Straight Sword - boss drop", "Ornamental Straight Sword", missable=True, boss=True),
        ERLocationData("CA: Golden Beast Crest Shield - boss drop", "Golden Beast Crest Shield", missable=True, boss=True),
    ],
    # MARK: Limgrave
    "Stranded Graveyard":[
        ERLocationData("LG/SG: Strength! - after cave of knowledge boss", "Strength!"),
        ERLocationData("LG/SG: Tarnished's Furled Finger - beside grace", "Tarnished's Furled Finger"),
        ERLocationData("LG/SG: Finger Severer - beside grace", "Finger Severer"),
    ],
    "Fringefolk Hero's Grave":[
        ERLocationData("LG/FHG: Poisonbone Dart x5 - top of first ramp", "Poisonbone Dart x5"),
        ERLocationData("LG/FHG: Golden Rune [5] - middle of second ramp pit", "Golden Rune [5]"),
        ERLocationData("LG/FHG: Lightning Grease x2 - drop into second ramp pit, left of fire spitter", "Lightning Grease x2"),
        ERLocationData("LG/FHG: Erdtree's Favor - altar by miniboss duo", "Erdtree's Favor"),
        ERLocationData("LG/FHG: Stonesword Key - drop into second ramp pit, past fire spitter, drop to bottom of big room", "Stonesword Key"),
        ERLocationData("LG/FHG: Erdtree Greatbow - kill chariot", "Erdtree Greatbow", drop=True, missable=True), #requires shackle or bow
        ERLocationData("LG/FHG: Great Arrow x10 - kill chariot", "Great Arrow x10", drop=True, missable=True), #requires shackle or bow
        ERLocationData("LG/FHG: Dragonwound Grease - top of third ramp", "Dragonwound Grease"),
        ERLocationData("LG/FHG: Dragon Communion Seal - nnemy drop top of third ramp", "Dragon Communion Seal", drop=True),
        ERLocationData("LG/FHG: Grave Glovewort [1] - middle of lower third ramp", "Grave Glovewort [1]"),
        ERLocationData("LG/FHG: Golden Seed - boss drop", "Golden Seed", boss=True),
        ERLocationData("LG/FHG: Banished Knight Oleg - boss drop", "Banished Knight Oleg", boss=True),
    ],
    "Limgrave":[ # World locations
        # misc stuff
        ERLocationData("LG/SG: Silver-Pickled Fowl Foot x2 - hidden drop down behind SG entrance", "Silver-Pickled Fowl Foot x2", hidden=True),
        ERLocationData("LG/TFS: Golden Halberd - first field boss", "Golden Halberd", boss=True),
        ERLocationData("LG/CE: Golden Rune [1] - to E", "Golden Rune [1]"),
        ERLocationData("LG/GC: Kukri x4 - to E", "Kukri x4"),
        ERLocationData("LG/SC: Crossed Legs - on ruin above", "Crossed Legs"),
        ERLocationData("LG/SC: Starlight Shards - cliff above to W", "Starlight Shards"),
        ERLocationData("LG/SG: Golden Seed - golden tree to W", "Golden Seed", prominent=True),
        ERLocationData("LG/SS: Smithing Stone [1] x3 - to SE", "Smithing Stone [1] x3"),
        ERLocationData("LG/SS: Ash of War: Wild Strikes - scarab to NW", "Ash of War: Wild Strikes", scarab=True),
        ERLocationData("LG/MCV: Reduvia - npc invader to E", "Reduvia", hostile_npc=True),
        ERLocationData("LG/MR: Sacrificial Twig - W of MR", "Sacrificial Twig"),
        ERLocationData("LG/MR: Golden Rune [1] - N of MR", "Golden Rune [1]"),
        ERLocationData("LG/TCM: Ash of War: Sacred Blade - scarab to N", "Ash of War: Sacred Blade", scarab=True),
        ERLocationData("LG/TCM: Neutralizing Boluses - to NE", "Neutralizing Boluses"),
        ERLocationData("LG/AS: Somber Smithing Stone [1] - scarab to W", "Somber Smithing Stone [1]", scarab=True),
        ERLocationData("LG/MCO: Golden Rune [2] - to W", "Golden Rune [2]"),
        ERLocationData("LG/MCO: Armorer's Cookbook [1] - to SW", "Armorer's Cookbook [1]"),
        ERLocationData("LG/MCO: Poisonbloom x2 - to NE", "Poisonbloom x2"),
        ERLocationData("LG/HC: Turtle Neck Meat - N above HC", "Turtle Neck Meat"),
        ERLocationData("LG/DC: Golden Rune [3] - E of DC", "Golden Rune [3]"),
        ERLocationData("LG/DC: Lance Talisman - NE of DC", "Lance Talisman"),

        # Near CC
        ERLocationData("LG/CC: Gold-Pickled Fowl Foot - to SE along beach", "Gold-Pickled Fowl Foot"),
        ERLocationData("LG/CC: Land Octopus Ovary - to NW along beach", "Land Octopus Ovary"),
        ERLocationData("LG/CC: Strip of White Flesh - to NW along beach", "Strip of White Flesh"),
        ERLocationData("LG/CC: Ash of War: Stamp (Sweep) - scarab to NW along beach", "Ash of War: Stamp (Sweep)"),
        # shop
        ERLocationData("LG/CC: Neutralizing Boluses x5 - Nomadic Merchant to SE", "Neutralizing Boluses x5", shop=True),
        ERLocationData("LG/CC: Stanching Boluses x3 - Nomadic Merchant to SE", "Stanching Boluses x3", shop=True),
        ERLocationData("LG/CC: Stimulating Boluses x2 - Nomadic Merchant to SE", "Stimulating Boluses x2", shop=True),
        ERLocationData("LG/CC: Smithing Stone [1] x3 - Nomadic Merchant to SE", "Smithing Stone [1] x3", shop=True),
        ERLocationData("LG/CC: Armorer's Cookbook [2] - Nomadic Merchant to SE", "Armorer's Cookbook [2]", shop=True),
        ERLocationData("LG/CC: Broadsword - Nomadic Merchant to SE", "Broadsword", shop=True),
        ERLocationData("LG/CC: Club - Nomadic Merchant to SE", "Club", shop=True),
        ERLocationData("LG/CC: Shortbow - Nomadic Merchant to SE", "Shortbow", shop=True),
        #ERLocationData("LG: Arrow - Nomadic Merchant to SE", "Arrow", shop=True),
        #ERLocationData("LG: Bolt - Nomadic Merchant to SE", "Bolt", shop=True),
        ERLocationData("LG/CC: Iron Roundshield - Nomadic Merchant to SE", "Iron Roundshield", shop=True),
        ERLocationData("LG/CC: Note: Land Squirts - Nomadic Merchant to SE", "Note: Land Squirts", shop=True),
        ERLocationData("LG/CC: Note: Stonedigger Trolls - Nomadic Merchant to SE", "Note: Stonedigger Trolls", shop=True),
        # Near WR
        ERLocationData("LG/WR: Greataxe - Carriage W of WR", "Greataxe"),
        ERLocationData("LG/WR: Gold-Pickled Fowl Foot - NW of WR", "Gold-Pickled Fowl Foot"),
        ERLocationData("LG/WR: Smoldering Butterfly x4 - SW of WR", "Smoldering Butterfly x4"),
        ERLocationData("LG/WR: Glintstone Staff - enemy drop S of WR under ruin", "Glintstone Staff", drop=True),
        ERLocationData("LG/WR: Golden Rune [1] 1 - graveyard S of WR", "Golden Rune [1]"),
        ERLocationData("LG/WR: Golden Rune [1] 2 - graveyard S of WR", "Golden Rune [1]"),
        ERLocationData("LG/WR: Golden Rune [1] 3 - graveyard S of WR", "Golden Rune [1]"),
        ERLocationData("LG/WR: Golden Rune [2] - graveyard S of WR", "Golden Rune [2]"),
        ERLocationData("LG/WR: Golden Rune [3] - graveyard S of WR", "Golden Rune [3]"),
        # Near ALN grace
        ERLocationData("LG/ALN: Mushroom x10 - Boc to SE", "Mushroom x10", missable=True),
        ERLocationData("LG/ALN: Arteria Leaf - to SE", "Arteria Leaf"),
        ERLocationData("LG/ALN: Ash of War: Determination - scarab to SE", "Ash of War: Determination", scarab=True),
        ERLocationData("LG/ALN: Smithing Stone [1] - bridge to SE", "Smithing Stone [1]"),
        ERLocationData("LG/ALN: Fire Grease - uder bridge to SE", "Fire Grease"),
        ERLocationData("LG/ALN: Ash of War: Repeating Thrust - night boss drop to SE", "Ash of War: Repeating Thrust", boss=True),
        ERLocationData("LG/ALN: Somber Smithing Stone [1] - after bridge to SE", "Somber Smithing Stone [1]"),
        # Near ALS grace
        ERLocationData("LG/ALS: Ash of War: Unsheathe - scarab to NW", "Ash of War: Unsheathe", scarab=True),
        ERLocationData("LG/ALS: Crab Eggs - to NW", "Crab Eggs"),
        ERLocationData("LG/ALS: Sliver of Meat - to W", "Sliver of Meat"),
        ERLocationData("LG/ALS: Golden Rune [2] - to S", "Golden Rune [2]"),
        ERLocationData("LG/ALS: Larval Tear - transforming enemy to E", "Larval Tear"),
        ERLocationData("LG/ALS: Golden Rune [1] - to SE high on cliff", "Golden Rune [1]"),
        ERLocationData("LG/ALS: Starlight Shards - to SE high on cliff", "Starlight Shards"),
        ERLocationData("LG/ALS: Royal House Scroll - to E on ruin", "Royal House Scroll"),
        ERLocationData("LG/ALS: Golden Rune [1] - to E", "Golden Rune [1]"),
        ERLocationData("LG/ALS: Great Épée - to E in chest", "Great Épée"),
        # Near Forlorn Hound Evergaol
        ERLocationData("LG/FHE: Large Club - S of Evergoal", "Large Club"),
        ERLocationData("LG/FHE: Ruin Fragment x3 - SW of Evergoal", "Ruin Fragment x3"),
        # Near SR grace
        ERLocationData("LG/SR: Crab Eggs - to S", "Crab Eggs"),
        ERLocationData("LG/SR: Slumbering Egg - to E on ruin", "Slumbering Egg"),
        ERLocationData("LG/SR: Golden Rune [1] - to N", "Golden Rune [1]"),
        ERLocationData("LG/SR: Lump of Flesh x3 - lower beach to W", "Lump of Flesh x3"),
        ERLocationData("LG/SR: Ash of War: Gravitas - enemy drop lower beach to NW", "Ash of War: Gravitas", drop=True),
        ERLocationData("LG/SR: Haligdrake Talisman - cave enterance lower beach to NW", "Haligdrake Talisman"),
        ERLocationData("LG/SR: Incantation Scarab - \"Homing Instinct\" Painting reward to NW", "Incantation Scarab"),
        # Near DBR
        ERLocationData("LG/DBR: Smithing Stone [1] - W of DBR", "Smithing Stone [1]"),
        ERLocationData("LG/DBR: Arteria Leaf - NE of DBR", "Arteria Leaf"),
        ERLocationData("LG/DBR: Dragon Heart - boss drop N of DBR", "Dragon Heart", boss=True),
        # Near MO grace
        ERLocationData("LG/MO: Magic Grease - to NE", "Magic Grease"),
        ERLocationData("LG/MO: Golden Rune [1] - on ruin to SW", "Golden Rune [1]"),
        ERLocationData("LG/MO: Golden Rune [5] - to SE", "Golden Rune [5]"),
        ERLocationData("LG/MO: Throwing Dagger x5 - to SE", "Throwing Dagger x5"),
        ERLocationData("LG/MO: Gold-Tinged Excrement x5 - to SE", "Gold-Tinged Excrement x5"),

        # Kenneth Haight
        ERLocationData("LG/MO: Erdsteel Dagger - kill FH enemy Kenneth Haight to NE", "Erdsteel Dagger", missable=True),
        ERLocationData("LG/MO: Golden Seed - kill Kenneth Haight to NE", "Golden Seed", npc=True),

        # Near SRW
        ERLocationData("LG/SRW: Map: Limgrave, East - map pillar W of SRW", "Map: Limgrave, East", prominent=True),
        ERLocationData("LG/SRW: Nomadic Warrior's Cookbook [4] - W of SRW", "Nomadic Warrior's Cookbook [4]"),
        ERLocationData("LG/SRW: Strip of White Flesh x3 - of SRW", "Strip of White Flesh x3"),
        # Near ME Minor Erdtree
        ERLocationData("LG/ME: Ash of War: Ground Slam - W of Minor Erdtree", "Ash of War: Ground Slam", scarab=True),
        ERLocationData("LG/ME: Thin Beast Bones x3 - W of Minor Erdtree", "Thin Beast Bones x3"),
        # shop
        ERLocationData("LG/ME: Festering Bloody Finger x5 - Nomadic Merchant S of Minor Erdtree", "Festering Bloody Finger x5", shop=True),
        ERLocationData("LG/ME: Sliver of Meat x5 - Nomadic Merchant S of Minor Erdtree", "Sliver of Meat x5", shop=True),
        ERLocationData("LG/ME: Beast Liver x5 - Nomadic Merchant S of Minor Erdtree", "Beast Liver x5", shop=True),
        ERLocationData("LG/ME: Lump of Flesh x3 - Nomadic Merchant S of Minor Erdtree", "Lump of Flesh x3", shop=True),
        ERLocationData("LG/ME: Trina's Lily x3 - Nomadic Merchant S of Minor Erdtree", "Trina's Lily x3", shop=True),
        ERLocationData("LG/ME: Smithing Stone [1] x3 - Nomadic Merchant S of Minor Erdtree", "Smithing Stone [1] x3", shop=True),
        ERLocationData("LG/ME: Nomadic Warrior's Cookbook [5] - Nomadic Merchant S of Minor Erdtree", "Nomadic Warrior's Cookbook [5]", shop=True),
        ERLocationData("LG/ME: Armorer's Cookbook [3] - Nomadic Merchant S of Minor Erdtree", "Armorer's Cookbook [3]", shop=True),
        ERLocationData("LG/ME: Hand Axe - Nomadic Merchant S of Minor Erdtree", "Hand Axe", shop=True),
        ERLocationData("LG/ME: St. Trina's Arrow x10 - Nomadic Merchant S of Minor Erdtree", "St. Trina's Arrow x10", shop=True),
        ERLocationData("LG/ME: Riveted Wooden Shield - Nomadic Merchant S of Minor Erdtree", "Riveted Wooden Shield", shop=True),
        ERLocationData("LG/ME: Blue-Gold Kite Shield - Nomadic Merchant S of Minor Erdtree", "Blue-Gold Kite Shield", shop=True),

        # Near FHW
        ERLocationData("LG/FHW: Golden Seed - golden tree to E", "Golden Seed", prominent=True),
        ERLocationData("LG/FHW: Golden Rune [1] - beach to SW", "Golden Rune [1]"),
        ERLocationData("LG/FHW: Golden Rune [1] 1 - graveyard to SW", "Golden Rune [1]"),
        ERLocationData("LG/FHW: Golden Rune [1] 2 - graveyard to SW", "Golden Rune [1]"),
        ERLocationData("LG/FHW: Golden Rune [1] 3 - graveyard to SW", "Golden Rune [1]"),
        ERLocationData("LG/FHW: Golden Rune [1] 4 - graveyard to SW", "Golden Rune [1]"),
        ERLocationData("LG/FHW: Golden Rune [2] 1 - graveyard to SW", "Golden Rune [2]"),
        ERLocationData("LG/FHW: Golden Rune [2] 2 - graveyard to SW", "Golden Rune [2]"),
        ERLocationData("LG/FHW: Golden Rune [3] - graveyard to SW", "Golden Rune [3]"),
        ERLocationData("LG/FHW: Golden Rune [4] - graveyard to SW", "Golden Rune [4]"),
        # Near SB
        ERLocationData("LG/SB: Smithing Stone [1] x2 - on bridge to E", "Smithing Stone [1] x2"),
        ERLocationData("LG/SB: Golden Rune [1] - past bridge to SE", "Golden Rune [1]"),
        ERLocationData("LG/SB: Smithing Stone [1] - to S", "Smithing Stone [1]"),
        # shop
        ERLocationData("LG/SB: Pickled Turtle Neck x3 - Nomadic Merchant to E", "Pickled Turtle Neck x3", shop=True),
        ERLocationData("LG/SB: Smithing Stone [1] x3 - Nomadic Merchant to E", "Smithing Stone [1] x3", shop=True),
        ERLocationData("LG/SB: Cracked Pot - Nomadic Merchant to E", "Cracked Pot", shop=True),
        ERLocationData("LG/SB: Nomadic Warrior's Cookbook [3] - Nomadic Merchant to E", "Nomadic Warrior's Cookbook [3]", shop=True),
        ERLocationData("LG/SB: Short Sword - Nomadic Merchant to E", "Short Sword", shop=True),
        ERLocationData("LG/SB: Halberd - Nomadic Merchant to E", "Halberd", shop=True),
        ERLocationData("LG/SB: Bandit Mask - Nomadic Merchant to E", "Bandit Mask", shop=True),
        ERLocationData("LG/SB: Note: Flame Chariots - Nomadic Merchant to E", "Note: Flame Chariots", shop=True),
        # Near SWVO  summonwater village outskirts
        ERLocationData("LG/SWVO: Fevor's Cookbook [1] - graveyard to S", "Fevor's Cookbook [1]"),
        ERLocationData("LG/SWVO: Golden Rune [1] 1 - graveyard to S", "Golden Rune [1]"),
        ERLocationData("LG/SWVO: Golden Rune [1] 2 - graveyard to S", "Golden Rune [1]"),
        ERLocationData("LG/SWVO: Golden Rune [1] 3 - graveyard to S", "Golden Rune [1]"),
        ERLocationData("LG/SWVO: Golden Rune [2] - graveyard to S", "Golden Rune [2]"),
        ERLocationData("LG/SWVO: Golden Rune [4] 1 - graveyard to S", "Golden Rune [4]"),
        ERLocationData("LG/SWVO: Golden Rune [4] 2 - graveyard to S", "Golden Rune [4]"),
        ERLocationData("LG/SWVO: Golden Rune [6] - graveyard to S", "Golden Rune [6]"),
        # Near SWV
        ERLocationData("LG/SWV: Smithing Stone [2] - down S of SMV", "Smithing Stone [2]"),
        ERLocationData("LG/SWV: Golden Rune [1] 1 - graveyard SE of SMV", "Golden Rune [1]"),
        ERLocationData("LG/SWV: Golden Rune [1] 2 - graveyard SE of SMV", "Golden Rune [1]"),
        ERLocationData("LG/SWV: Golden Rune [1] 3 - graveyard SE of SMV", "Golden Rune [1]"),
        ERLocationData("LG/SWV: Golden Rune [1] 4 - graveyard SE of SMV", "Golden Rune [1]"),
        ERLocationData("LG/SWV: Golden Rune [1] 5 - graveyard SE of SMV", "Golden Rune [1]"),
        ERLocationData("LG/SWV: Golden Rune [2] - graveyard SE of SMV", "Golden Rune [2]"),
        ERLocationData("LG/SWV: Golden Rune [5] - graveyard SE of SMV", "Golden Rune [5]"),
        ERLocationData("LG/SWV: Golden Rune [4] - ruins NE of SMV", "Golden Rune [4]"),
        
        # LG Evergaols
        ERLocationData("LG/SE: Aspects of the Crucible: Tail - Stormhill Evergaol", "Aspects of the Crucible: Tail", boss=True),
        ERLocationData("LG/FHE: Bloodhound's Fang - Forlorn Hound Evergaol", "Bloodhound's Fang", boss=True),

        ERLocationData("LG/ME: Spiked Cracked Tear - Minor Erdtree", "Spiked Cracked Tear", prominent=True),
        ERLocationData("LG/ME: Greenspill Crtstal Tear - Minor Erdtree", "Greenspill Crtstal Tear", prominent=True),
    ],# MARK: LG Locations
    "Church of Elleh":[
        ERLocationData("LG/(CE): Smithing Stone [1] - on anvil", "Smithing Stone [1]"),
        ERLocationData("LG/(CE): Golden Rune [2] - out front", "Golden Rune [2]"),
        # Kalé shop
        ERLocationData("LG/(CE): Finger Snap - kill Kalé or Blaidd quest", "Finger Snap", npc=True), #idk how Blaidd quest works tbh, just hear howl, talk to kale get finger, finger at howl, blaidd appera
        #ERLocationData("LG/(CE): Throwing Dagger - Kalé Shop", "Throwing Dagger", shop=True),
        ERLocationData("LG/(CE): Telescope - Kalé Shop", "Telescope", shop=True),
        ERLocationData("LG/(CE): Furlcalling Finger Remedy - Kalé Shop", "Furlcalling Finger Remedy", shop=True),
        ERLocationData("LG/(CE): Cracked Pot x3 - Kalé Shop", "Cracked Pot x3", shop=True),
        ERLocationData("LG/(CE): Crafting Kit - Kalé Shop", "Crafting Kit", shop=True),
        ERLocationData("LG/(CE): Nomadic Warrior's Cookbook [1] - Kalé Shop", "Nomadic Warrior's Cookbook [1]", shop=True),
        ERLocationData("LG/(CE): Nomadic Warrior's Cookbook [2] - Kalé Shop", "Nomadic Warrior's Cookbook [2]", shop=True),
        ERLocationData("LG/(CE): Missionary's Cookbook [1] - Kalé Shop", "Missionary's Cookbook [1]", shop=True),
        #ERLocationData("LG/(CE): Arrow - Kalé Shop", "Arrow", shop=True),
        #ERLocationData("LG/(CE): Bolt - Kalé Shop", "Bolt", shop=True),
        ERLocationData("LG/(CE): Torch - Kalé Shop", "Torch", shop=True),
        ERLocationData("LG/(CE): Large Leather Shield - Kalé Shop", "Large Leather Shield", shop=True),
        ERLocationData("LG/(CE): Chain Coif - Kalé Shop", "Chain Coif", shop=True),
        ERLocationData("LG/(CE): Chain Armor - Kalé Shop", "Chain Armor", shop=True),
        ERLocationData("LG/(CE): Gauntlets - Kalé Shop", "Gauntlets", shop=True),
        ERLocationData("LG/(CE): Chain Leggings - Kalé Shop", "Chain Leggings", shop=True),
        ERLocationData("LG/(CE): Note: Flask of Wondrous Physick - Kalé Shop", "Note: Flask of Wondrous Physick", shop=True),
        ERLocationData("LG/(CE): Note: Waypoint Ruins - Kalé Shop", "Note: Waypoint Ruins", shop=True),
        # Ranni
        ERLocationData("LG/(CE): Spirit Calling Bell - Ranni", "Spirit Calling Bell", prominent=True),
        ERLocationData("LG/(CE): Lone Wolf Ashes - Ranni", "Lone Wolf Ashes"),
    ],
    "Coastal Cave":[
        ERLocationData("LG/(CC): Land Octopus Ovary - before boss", "Land Octopus Ovary"),
        ERLocationData("LG/(CC): Sewing Needle - boss drop", "Sewing Needle", boss=True),
        ERLocationData("LG/(CC): Tailoring Tools - boss drop", "Tailoring Tools", boss=True),
        ERLocationData("LG/(CC): Smoldering Butterfly - after boss", "Smoldering Butterfly"),
    ],
    "Church of Dragon Communion":[
        ERLocationData("LG/(CDC): Great Dragonfly Head x4 - to W", "Great Dragonfly Head x4"),
        ERLocationData("LG/(CDC): Exalted Flesh - to S up high", "Exalted Flesh"),
        ERLocationData("LG/(CDC): Smithing Stone [2] - to S", "Smithing Stone [2]"),
        ERLocationData("LG/(CDC): Somber Smithing Stone [1] - scarab to S", "Somber Smithing Stone [1]", scarab=True),
    ],
    "Groveside Cave":[
        ERLocationData("LG/(GC): Cracked Pot - first room", "Cracked Pot"),
        ERLocationData("LG/(GC): Glowstone x3 - first room", "Glowstone x3"),
        ERLocationData("LG/(GC): Golden Rune [1] - first room", "Golden Rune [1]"),
        ERLocationData("LG/(GC): Flamedrake Talisman - boss drop", "Flamedrake Talisman", boss=True),
    ],
    "Stormfoot Catacombs":[
        ERLocationData("LG/(SC): Root Resin x2 - first room", "Root Resin x2"),
        ERLocationData("LG/(SC): Prattling Pate \"Hello\" - behind first fire spitter", "Prattling Pate \"Hello\""),
        ERLocationData("LG/(SC): Smoldering Butterfly x3 - behind second fire spitter", "Smoldering Butterfly x3"),
        ERLocationData("LG/(SC): Wandering Noble Ashes - room at end of hall after latter", "Wandering Noble Ashes"),
        ERLocationData("LG/(SC): Noble Sorcerer Ashes - boss drop", "Noble Sorcerer Ashes"),
    ],
    "Gatefront Ruins":[
        ERLocationData("LG/(GR): Lordsworn's Greatsword - NW carriage", "Lordsworn's Greatsword"),
        ERLocationData("LG/(GR): Map: Limgrave, West - map pillar", "Map: Limgrave, West", prominent=True),
        ERLocationData("LG/(GR): Ruin Fragment x3 - S of NW carriage", "Ruin Fragment x3"),
        ERLocationData("LG/(GR): Flail - NE carriage", "Flail"),
        ERLocationData("LG/(GR): Ash of War: Storm Stomp - underground chest", "Ash of War: Storm Stomp"),
        ERLocationData("LG/(GR): Whetstone Knife - underground chest", "Whetstone Knife", prominent=True),
    ],
    "Limgrave Tunnels":[
        ERLocationData("LG/(LT): Golden Rune [4] - off side of entrance elevator", "Golden Rune [4]"),
        ERLocationData("LG/(LT): Smithing Stone [1] - room with rats", "Smithing Stone [1]"),
        ERLocationData("LG/(LT): Glintstone Scrap x3 - off side of second elevator", "Glintstone Scrap x3"),
        ERLocationData("LG/(LT): Large Glintstone Scrap x5 - room after second elevator", "Large Glintstone Scrap x5"),
        ERLocationData("LG/(LT): Golden Rune [1] - off side of third elevator", "Golden Rune [1]"),
        ERLocationData("LG/(LT): Roar Medallion - boss drop", "Roar Medallion", boss=True),
    ],
    "Stormgate":[
        ERLocationData("LG/(SG): Lump of Flesh - lower area", "Lump of Flesh"),
        ERLocationData("LG/(SG): Golden Rune [1] - lower area", "Golden Rune [1]"),
        ERLocationData("LG/(SG): Smoldering Butterfly x5 - on cliff above", "Smoldering Butterfly x5"),
        ERLocationData("LG/(SG): Arrow's Reach Talisman - chest above gate", "Arrow's Reach Talisman"),
        ERLocationData("LG/(SG): Golden Rune [2] - off side of ruin above", "Golden Rune [2]"),
    ],
    "Stormhill Shack":[
        ERLocationData("LG/(SS): Stonesword Key - near grace", "Stonesword Key"),
    ],
    "Waypoint Ruins":[
        ERLocationData("LG/(WR): Golden Rune [1] - within ruins", "Golden Rune [1]"),
        ERLocationData("LG/(WR): Immunizing Cured Meat - within ruins", "Immunizing Cured Meat"),
        ERLocationData("LG/(WR): Glowstone x2 - within ruins", "Glowstone x2"),
        ERLocationData("LG/(WR): Trina's Lily x4 - on ruin wall", "Trina's Lily x4"),
        #Sellen shop
        ERLocationData("LG/(WR): Nod In Thought - Sellen", "Nod In Thought"),
        ERLocationData("LG/(WR): Glintstone Pebble - Sellen Shop", "Glintstone Pebble", shop=True),
        ERLocationData("LG/(WR): Glintstone Stars - Sellen Shop", "Glintstone Stars", shop=True),
        ERLocationData("LG/(WR): Glintstone Arc - Sellen Shop", "Glintstone Arc", shop=True),
        ERLocationData("LG/(WR): Crystal Barrage - Sellen Shop", "Crystal Barrage", shop=True),
        ERLocationData("LG/(WR): Scholar's Armament - Sellen Shop", "Scholar's Armament", shop=True),
        ERLocationData("LG/(WR): Scholar's Shield - Sellen Shop", "Scholar's Shield", shop=True),
    ],
    "Dragon-Burnt Ruins":[
        ERLocationData("LG/(DBR): Crab Eggs - wthin ruins", "Crab Eggs"),
        ERLocationData("LG/(DBR): Stonesword Key - within ruined building", "Stonesword Key"),
        ERLocationData("LG/(DBR): Golden Rune [2] - within ruins", "Golden Rune [2]"),
        ERLocationData("LG/(DBR): Twinblade - underground chest hidden within ruin", "Twinblade", hidden=True),
    ],
    "Murkwater Cave":[
        ERLocationData("LG/(MCave): Mushroom x5 - chest at back", "Mushroom x5"),
        ERLocationData("LG/(MCave): Cloth Garb - Patches chest", "Cloth Garb"),
        ERLocationData("LG/(MCave): Cloth Trousers - Patches chest", "Cloth Trousers"),
        # patches
        ERLocationData("LG/(MCave): Golden Rune [1] x2 - spare or kill Patches", "Golden Rune [1] x2"),
        ERLocationData("LG/(MCave): Grovel For Mercy - spare Patches", "Grovel For Mercy", missable=True),

        ERLocationData("LG/(MCave): Spear +7 - kill Patches", "Spear", missable=True, npc=True),
        ERLocationData("LG/(MCave): Leather Armor - kill Patches", "Leather Armor", missable=True, npc=True),
        ERLocationData("LG/(MCave): Leather Gloves - kill Patches", "Leather Gloves", missable=True, npc=True),
        ERLocationData("LG/(MCave): Leather Boots - kill Patches", "Leather Boots", missable=True, npc=True),

        ERLocationData("LG/(MCave): Extreme Repentance - grovel emote Patches", "Extreme Repentance", missable=True),
        ERLocationData("LG/(MCave): Calm Down! - trapped chest", "Calm Down!", missable=True),

        ERLocationData("LG/(MCave): Gold-Pickled Fowl Foot x3 - Patches Shop", "Gold-Pickled Fowl Foot x3"),
        ERLocationData("LG/(MCave): Fan Daggers x20 - Patches Shop", "Fan Daggers x20"),
        ERLocationData("LG/(MCave): Margit's Shackle - Patches Shop", "Margit's Shackle"),
        ERLocationData("LG/(MCave): Grace Mimic x15 - Patches Shop", "Grace Mimic x15"),
        ERLocationData("LG/(MCave): Furlcalling Finger Remedy x3 - Patches Shop", "Furlcalling Finger Remedy x3"),
        ERLocationData("LG/(MCave): Festering Bloody Finger x5 - Patches Shop", "Festering Bloody Finger x5"),
        ERLocationData("LG/(MCave): Stonesword Key - Patches Shop", "Stonesword Key"),
        ERLocationData("LG/(MCave): Missionary's Cookbook [2] - Patches Shop", "Missionary's Cookbook [2]"),
        ERLocationData("LG/(MCave): Parrying Dagger - Patches Shop", "Parrying Dagger"),
        ERLocationData("LG/(MCave): Great Arrow x10 - Patches Shop", "Great Arrow x10"),
        ERLocationData("LG/(MCave): Ballista Bolt x5 - Patches Shop", "Ballista Bolt x5"),
        ERLocationData("LG/(MCave): Horse Crest Wooden Shield - Patches Shop", "Horse Crest Wooden Shield"),
        ERLocationData("LG/(MCave): Sacrificial Twig - Patches Shop", "Sacrificial Twig"),
    ],
    "Mistwood Ruins":[
        ERLocationData("LG/(MR): Smithing Stone [2] - chest in ruins", "Smithing Stone [2]"),
        ERLocationData("LG/(MR): Axe Talisman - chest underground", "Axe Talisman"),
        ERLocationData("LG/(MR): Golden Rune [2] - within ruins", "Golden Rune [2]"),
    ],
    "Fort Haight":[
        ERLocationData("LG/(FH): Bloodrose x3 - near enterance", "Bloodrose x3"),
        ERLocationData("LG/(FH): Nomadic Warrior's Cookbook [6] - ground floor room", "Nomadic Warrior's Cookbook [6]"),
        ERLocationData("LG/(FH): Ash of War: Bloody Slash - enemy drop upper area", "Ash of War: Bloody Slash", drop=True),
        ERLocationData("LG/(FH): Bloodrose x5 - upper area", "Bloodrose x5"),
        ERLocationData("LG/(FH): Smithing Stone [1] - catwalk right of tower", "Smithing Stone [1]"),
        ERLocationData("LG/(FH): Dectus Medallion (Left) - tower chest", "Dectus Medallion (Left)", prominent=True),
    ],
    "Third Church of Marika":[
        ERLocationData("LG/(TCM): Flask of Wondrous Physick - in basin", "Flask of Wondrous Physick", prominent=True),
        ERLocationData("LG/(TCM): Crimson Crystal Tear - in basin", "Crimson Crystal Tear", prominent=True),
        ERLocationData("LG/(TCM): Sacred Tear - by statue", "Sacred Tear", prominent=True),
    ],
    "LG Artist's Shack":[
        ERLocationData("LG/(AS): \"Homing Instinct\" Painting - painting", "\"Homing Instinct\" Painting"),
        ERLocationData("LG/(AS): Smithing Stone [1] - on corpse", "Smithing Stone [1]"),
    ],
    "Summonwater Village":[
        ERLocationData("LG/(SWV): Mushroom x3 - within ruins", "Mushroom x3"),
        ERLocationData("LG/(SWV): Smithing Stone [1] - N side", "Smithing Stone [1]"),
        ERLocationData("LG/(SWV): Green Turtle Talisman - behind imp statue", "Green Turtle Talisman"),
        ERLocationData("LG/(SWV): Deathroot - boss drop", "Deathroot", boss=True),
        ERLocationData("LG/(SWV): Skeletal Militiaman Ashes - boss drop", "Skeletal Militiaman Ashes", boss=True),
    ],
    "Murkwater Catacombs":[
        ERLocationData("LG/(MCC): Root Resin x5 - by lever", "Root Resin x5"),
        ERLocationData("LG/(MCC): Banished Knight Engvall - boss drop", "Banished Knight Engvall", boss=True),
    ],
    "Highroad Cave":[
        ERLocationData("LG/(HC): Golden Rune [1] - past second hole", "Golden Rune [1]"),
        ERLocationData("LG/(HC): Arteria Leaf x3 - on ledge before water area", "Arteria Leaf x3"),
        ERLocationData("LG/(HC): Fire Grease x2 - below ledge before water area", "Fire Grease x2"),
        ERLocationData("LG/(HC): Smithing Stone [1] x3 - below water enterance ledge", "Smithing Stone [1] x3"),
        ERLocationData("LG/(HC): Smithing Stone [2] - top of small waterfall area", "Smithing Stone [2]"),
        ERLocationData("LG/(HC): Golden Rune [4] - top of small waterfall area", "Golden Rune [4]"),
        ERLocationData("LG/(HC): Shamshir - center of water area", "Shamshir"),
        ERLocationData("LG/(HC): Furlcalling Finger Remedy - past miniboss on ledge", "Furlcalling Finger Remedy"),
        ERLocationData("LG/(HC): Blue Dancer Charm - boss drop", "Blue Dancer Charm", boss=True),
    ],
    "Deathtouched Catacombs":[
        ERLocationData("LG/(DC): Bloodrose x3 - by lever", "Bloodrose x3"),
        ERLocationData("LG/(DC): Uchigatana - down small tunnel on ledge", "Uchigatana"),
        ERLocationData("LG/(DC): Assassin's Crimson Dagger - boss drop", "Assassin's Crimson Dagger", boss=True),
        ERLocationData("LG/(DC): Deathroot - boss chest", "Deathroot", boss=True),
    ],



    # ERLocationData(":  - ", ""),
    # MARK: Liurnia of The Lakes
    "Liurnia of The Lakes":[
    ],

    "Chapel of Anticipation [Return]":[
        ERLocationData("CA Return: The Stormhawk King - top of church", "The Stormhawk King"),
        ERLocationData("CA Return: Stormhawk Deenh - chest top of church", "Stormhawk Deenh"),
    ],

    # MARK: Caelid
    "Caelid":[
    ],
    "Smoldering Church":[
        ERLocationData("CL/(SC): Sacred Scorpion Charm - kill invader", "Sacred Scorpion Charm", hostile_npc=True),
        ERLocationData("CL/(SC): Missionary's Cookbook [3] - on corpse", "Missionary's Cookbook [3]"),
        ERLocationData("CL/(SC): Nomadic Warrior's Cookbook [14] - on corpse", "Nomadic Warrior's Cookbook [14]"),
    ],

    # MARK: DLC Locations
    "Gravesite Plain":[
    ],
}

for i, region in enumerate(region_order + region_order_dlc):
    for location in location_tables[region]: location.region_value = i

for region in region_order_dlc:
    for location in location_tables[region]:
        location.dlc = True

for region in [# conditional ig
]:
    for location in location_tables[region]:
        location.conditional = True

location_name_groups: Dict[str, Set[str]] = {
    # We could insert these locations automatically with setdefault(), but we set them up explicitly
    # instead so we can choose the ordering.
    "Prominent": set(),
    "Progression": set(),
    "Main Boss Rewards": set(),
    "Boss Rewards": set(),
    "Hostile NPC Rewards": set(),
    "Friendly NPC Rewards": set(),
    "Scarab": set(),
    "Upgrade": set(),
    "Unique": set(),
    "Healing": set(),
    "Goods": set(),
    "Hidden": set(),
    "Weapons": set(),
    "Ash of war": set(),
    "Armor": set(),
    "Accessory": set(),
    "Missable": set(),
}

location_descriptions = {
    "Prominent": "A small number of locations that are in very obvious locations. Mostly boss " + \
                 "drops. Ideal for setting as priority locations.",
    "Progression": "Locations that contain items in vanilla which unlock other locations.",
    "Main Boss Rewards": "Great Runes.",
    "Boss Rewards": "Miniboss drops. Only includes enemies considered minibosses by the " + \
                        "enemy randomizer.",
    "Hostile NPC Rewards": "Drops from NPCs that are hostile to you. This includes scripted " + \
                           "invaders and initially-friendly NPCs that must be fought as part of their quest.",
    "Friendly NPC Rewards": "Items given by friendly NPCs as part of their quests or from " + \
                            "non-violent interaction.",
    "Upgrade": "Locations that contain upgrade items in vanilla, including titanite, gems, and " + \
               "Shriving Stones.",
    "Runes": "Locations that contain rune items in vanilla.",
    "Unique": "Locations that contain items in vanilla that are unique per NG cycle, such as " + \
              "scrolls, keys, ashes, and so on. Doesn't cover equipment, spells, or runes.",
    "Healing": "Locations that contain Undead Bone Shards and Estus Shards in vanilla.",
    "Goods": "Misc, Key, Spell, most stuff that goes into your inventory.",
    "Hidden": "Locations that are particularly difficult to find, such as behind illusory " + \
              "walls, down hidden drops, and so on. Does not include large locations.",
    "Weapons": "Locations that contain weapons in vanilla.",
    "Ash of war": "Locations that contain Ash of wars in vanilla.",
    "Armor": "Locations that contain armor in vanilla.",
    "Accessory": "Locations that contain accessories in vanilla.",
    "Spells": "Locations that contain spells in vanilla.",
    "Spirits": "Locations that contain spirits in vanilla.",
    "Missable": "Locations that can be missed in vanilla.",
}

location_dictionary: Dict[str, ERLocationData] = {}
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

temp = location_name_groups['Gravesite Plain'] # might work shrug
counter = 0
for location in region_order_dlc:
    if counter > 1:
        temp.union(location_name_groups[location])
    counter += 1

location_name_groups["DLC"] = temp