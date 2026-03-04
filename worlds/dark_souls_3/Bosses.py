# In almost all cases, we leave boss and enemy randomization up to the static randomizer. But for
# Yhorm specifically we need to know where he ends up in order to ensure that the Storm Ruler is
# available before his fight.

from dataclasses import dataclass, field
from typing import Set, Optional


@dataclass
class DS3BossInfo:
    """The set of locations a given boss location blocks access to."""

    name: str
    """The boss's name."""

    region: str
    """The region that this is the boss of."""

    id: int
    """The game's ID for this particular boss."""

    flag: Optional[int]
    """The event flag that's set when this boss is defeated.

    This is None for first-phase bosses."""

    dlc: bool = False
    """This boss appears in one of the game's DLCs."""

    before_storm_ruler: bool = False
    """Whether this location appears before it's possible to get Storm Ruler in vanilla.

    This is used to determine whether it's safe to place Yhorm here if weapons
    aren't randomized.
    """

    locations: Set[str] = field(default_factory=set)
    """Additional individual locations that can't be accessed until the boss is dead."""

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)


# Note: the static randomizer splits up some bosses into separate fights for separate phases, each
# of which can be individually replaced by Yhorm.
all_bosses = [
    DS3BossInfo(
        "Iudex Gundyr", "Cemetery of Ash", 4000800, 14000800,
        before_storm_ruler = True, locations = ["CA: Coiled Sword - boss drop"],
    ),
    DS3BossInfo(
        "Vordt of the Boreal Valley", "High Wall of Lothric", 3000800, 13000800,
        before_storm_ruler = True, locations = ["HWL: Soul of Boreal Valley Vordt"],
    ),
    DS3BossInfo(
        "Curse-rotted Greatwood", "Undead Settlement", 3100800, 13100800,
        locations = [
            "US: Soul of the Rotted Greatwood",
            "US: Transposing Kiln - boss drop",
            "US: Wargod Wooden Shield - Pit of Hollows",
            "FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
            "FS: Sunset Shield - by grave after killing Hodrick w/Sirris",
            "US: Sunset Helm - Pit of Hollows after killing Hodrick w/Sirris",
            "US: Sunset Armor - pit of hollows after killing Hodrick w/Sirris",
            "US: Sunset Gauntlets - pit of hollows after killing Hodrick w/Sirris",
            "US: Sunset Leggings - pit of hollows after killing Hodrick w/Sirris",
            "FS: Sunless Talisman - Sirris, kill GA boss",
            "FS: Sunless Veil - shop, Sirris quest, kill GA boss",
            "FS: Sunless Armor - shop, Sirris quest, kill GA boss",
            "FS: Sunless Gauntlets - shop, Sirris quest, kill GA boss",
            "FS: Sunless Leggings - shop, Sirris quest, kill GA boss",
        ],
    ),
    DS3BossInfo(
        "Crystal Sage", "Road of Sacrifices", 3300850, 13300850,
        locations = [
            "RS: Soul of a Crystal Sage",
            "FS: Sage's Big Hat - shop after killing RS boss",
            "FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
        ],
    ),
    DS3BossInfo(
        "Deacons of the Deep", "Cathedral of the Deep", 3500800, 13500800,
        locations = [
            "CD: Soul of the Deacons of the Deep",
            "CD: Small Doll - boss drop",
            "CD: Archdeacon White Crown - boss room after killing boss",
            "CD: Archdeacon Holy Garb - boss room after killing boss",
            "CD: Archdeacon Skirt - boss room after killing boss",
            "FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
        ],
    ),
    DS3BossInfo(
        "Abyss Watchers", "Farron Keep", 3300801, 13300800,
        before_storm_ruler = True, locations = [
            "FK: Soul of the Blood of the Wolf",
            "FK: Cinders of a Lord - Abyss Watcher",
            "FS: Undead Legion Helm - shop after killing FK boss",
            "FS: Undead Legion Armor - shop after killing FK boss",
            "FS: Undead Legion Gauntlet - shop after killing FK boss",
            "FS: Undead Legion Leggings - shop after killing FK boss",
            "FS: Farron Ring - Hawkwood",
            "FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
        ],
    ),
    DS3BossInfo(
        "High Lord Wolnir", "Catacombs of Carthus", 3800800, 13800800,
        before_storm_ruler = True, locations = [
            "CC: Soul of High Lord Wolnir",
            "FS: Wolnir's Crown - shop after killing CC boss",
            "CC: Homeward Bone - Irithyll bridge",
            "CC: Pontiff's Right Eye - Irithyll bridge, miniboss drop",
        ],
    ),
    DS3BossInfo(
        "Pontiff Sulyvahn", "Irithyll of the Boreal Valley", 3700850, 13700800,
        locations = ["IBV: Soul of Pontiff Sulyvahn"],
    ),
    DS3BossInfo(
        "Old Demon King", "Smouldering Lake", 3800830, 13800830,
        locations = ["SL: Soul of the Old Demon King"],
    ),
    DS3BossInfo(
        "Yhorm the Giant", "Profaned Capital", 3900800, 13900800,
        locations = [
            "PC: Soul of Yhorm the Giant",
            "PC: Cinders of a Lord - Yhorm the Giant",
            "PC: Siegbräu - Siegward after killing boss",
        ],
    ),
    DS3BossInfo(
        "Aldrich, Devourer of Gods", "Anor Londo", 3700800, 13700850,
        locations = [
            "AL: Soul of Aldrich",
            "AL: Cinders of a Lord - Aldrich",
            "FS: Smough's Helm - shop after killing AL boss",
            "FS: Smough's Armor - shop after killing AL boss",
            "FS: Smough's Gauntlets - shop after killing AL boss",
            "FS: Smough's Leggings - shop after killing AL boss",
            "AL: Sun Princess Ring - dark cathedral, after boss",
            "FS: Leonhard's Garb - shop after killing Leonhard",
            "FS: Leonhard's Gauntlets - shop after killing Leonhard",
            "FS: Leonhard's Trousers - shop after killing Leonhard",
        ],
    ),
    DS3BossInfo(
        "Dancer of the Boreal Valley", "Lothric Castle Entrance", 3000899, 13000890,
        locations = [
            "HWL: Soul of the Dancer",
            "FS: Dancer's Crown - shop after killing LC entry boss",
            "FS: Dancer's Armor - shop after killing LC entry boss",
            "FS: Dancer's Gauntlets - shop after killing LC entry boss",
            "FS: Dancer's Leggings - shop after killing LC entry boss",
        ],
    ),
    DS3BossInfo(
        "Dragonslayer Armour", "Lothric Castle End", 3010800, 13010800,
        locations = [
            "LC: Soul of Dragonslayer Armour",
            "FS: Morne's Helm - shop after killing Eygon or LC boss",
            "FS: Morne's Armor - shop after killing Eygon or LC boss",
            "FS: Morne's Gauntlets - shop after killing Eygon or LC boss",
            "FS: Morne's Leggings - shop after killing Eygon or LC boss",
            "LC: Titanite Chunk - down stairs after boss",
        ],
    ),
    DS3BossInfo(
        "Consumed King Oceiros", "Consumed King's Garden", 3000830, 13000830,
        locations = [
            "CKG: Soul of Consumed Oceiros",
            "CKG: Titanite Scale - tomb, chest #1",
            "CKG: Titanite Scale - tomb, chest #2",
            "CKG: Drakeblood Helm - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Armor - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Gauntlets - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Leggings - tomb, after killing AP mausoleum NPC",
        ],
    ),
    DS3BossInfo(
        "Champion Gundyr", "Untended Graves", 4000830, 14000830, locations = [
            "UG: Soul of Champion Gundyr",
            "FS: Gundyr's Helm - shop after killing UG boss",
            "FS: Gundyr's Armor - shop after killing UG boss",
            "FS: Gundyr's Gauntlets - shop after killing UG boss",
            "FS: Gundyr's Leggings - shop after killing UG boss",
            "UG: Hornet Ring - environs, right of main path after killing FK boss",
            "UG: Chaos Blade - environs, left of shrine",
            "UG: Blacksmith Hammer - shrine, Andre's room",
            "UG: Eyes of a Fire Keeper - shrine, Irina's room",
            "UG: Coiled Sword Fragment - shrine, dead bonfire",
            "UG: Soul of a Crestfallen Knight - environs, above shrine entrance",
            "UG: Life Ring+3 - shrine, behind big throne",
            "UG: Ring of Steel Protection+1 - environs, behind bell tower",
            "FS: Ring of Sacrifice - Yuria shop",
            "UG: Ember - shop",
            "UG: Priestess Ring - shop",
            "UG: Wolf Knight Helm - shop after killing FK boss",
            "UG: Wolf Knight Armor - shop after killing FK boss",
            "UG: Wolf Knight Gauntlets - shop after killing FK boss",
            "UG: Wolf Knight Leggings - shop after killing FK boss",
        ],
    ),
    DS3BossInfo(
        "Ancient Wyvern", "Archdragon Peak Fort", 3200800, 13200800,
        locations = ["AP: Dragon Head Stone - fort, boss drop"],
    ),
    DS3BossInfo(
        "King of the Storm", "Archdragon Peak End", 3200850, None,
        locations = [
            "AP: Soul of the Nameless King",
            "FS: Golden Crown - shop after killing AP boss",
            "FS: Dragonscale Armor - shop after killing AP boss",
            "FS: Golden Bracelets - shop after killing AP boss",
            "FS: Dragonscale Waistcloth - shop after killing AP boss",
            "AP: Titanite Slab - plaza",
            "AP: Covetous Gold Serpent Ring+2 - plaza",
            "AP: Dragonslayer Helm - plaza",
            "AP: Dragonslayer Armor - plaza",
            "AP: Dragonslayer Gauntlets - plaza",
            "AP: Dragonslayer Leggings - plaza",
        ],
    ),
    DS3BossInfo(
        "Nameless King", "Archdragon Peak End", 3200851, 13200850, locations = [
            "AP: Soul of the Nameless King",
            "FS: Golden Crown - shop after killing AP boss",
            "FS: Dragonscale Armor - shop after killing AP boss",
            "FS: Golden Bracelets - shop after killing AP boss",
            "FS: Dragonscale Waistcloth - shop after killing AP boss",
            "AP: Titanite Slab - plaza",
            "AP: Covetous Gold Serpent Ring+2 - plaza",
            "AP: Dragonslayer Helm - plaza",
            "AP: Dragonslayer Armor - plaza",
            "AP: Dragonslayer Gauntlets - plaza",
            "AP: Dragonslayer Leggings - plaza",
        ],
    ),
    DS3BossInfo(
        "Lothric, Younger Prince", "Grand Archives", 3410830, None,
        locations = [
            "GA: Soul of the Twin Princes",
            "GA: Cinders of a Lord - Lothric Prince",
            "FS: Lorian's Helm - shop after killing GA boss",
            "FS: Lorian's Armor - shop after killing GA boss",
            "FS: Lorian's Gauntlets - shop after killing GA boss",
            "FS: Lorian's Leggings - shop after killing GA boss",
        ],
    ),
    DS3BossInfo(
        "Lorian, Elder Prince", "Grand Archives", 3410832, 13410830,
        locations = [
            "GA: Soul of the Twin Princes",
            "GA: Cinders of a Lord - Lothric Prince",
            "FS: Lorian's Helm - shop after killing GA boss",
            "FS: Lorian's Armor - shop after killing GA boss",
            "FS: Lorian's Gauntlets - shop after killing GA boss",
            "FS: Lorian's Leggings - shop after killing GA boss",
        ],
    ),
    DS3BossInfo(
        "Champion's Gravetender and Gravetender Greatwolf",
        "Painted World of Ariandel Lower",
        4500860,
        14500860,
        dlc = True,
        locations = ["PW1: Valorheart - boss drop"],
    ),
    DS3BossInfo(
        "Sister Friede", "Painted World of Ariandel End", 4500801, None,
        dlc = True,
        locations = [
            "PW2: Soul of Sister Friede",
            "PW2: Titanite Slab - boss drop",
            "PW1: Titanite Slab - Corvian",
            "FS: Ordained Hood - shop after killing PW2 boss",
            "FS: Ordained Dress - shop after killing PW2 boss",
            "FS: Ordained Trousers - shop after killing PW2 boss",
        ],
    ),
    DS3BossInfo(
        "Blackflame Friede", "Painted World of Ariandel End", 4500800, 14500800,
        dlc = True, locations = [
            "PW2: Soul of Sister Friede",
            "PW1: Titanite Slab - Corvian",
            "FS: Ordained Hood - shop after killing PW2 boss",
            "FS: Ordained Dress - shop after killing PW2 boss",
            "FS: Ordained Trousers - shop after killing PW2 boss",
        ],
    ),
    DS3BossInfo(
        "Demon Prince", "Dreg Heap", 5000801, 15000800,
        dlc = True,
        locations = ["DH: Soul of the Demon Prince", "DH: Small Envoy Banner - boss drop"],
    ),
    DS3BossInfo(
        "Halflight, Spear of the Church", "Ringed City Midway", 5100800, 15100800,
        dlc = True,
        locations = [
            "RC: Titanite Slab - mid boss drop",
            "RC: Titanite Slab - ashes, NPC drop",
            "RC: Titanite Slab - ashes, mob drop",
            "RC: Filianore's Spear Ornament - mid boss drop",
            "RC: Crucifix of the Mad King - ashes, NPC drop",
            "RC: Shira's Crown - Shira's room after killing ashes NPC",
            "RC: Shira's Armor - Shira's room after killing ashes NPC",
            "RC: Shira's Gloves - Shira's room after killing ashes NPC",
            "RC: Shira's Trousers - Shira's room after killing ashes NPC",
        ],
    ),
    DS3BossInfo(
        "Darkeater Midir", "Ringed City Hidden", 5100850, 15100850,
        dlc = True,
        locations = [
            "RC: Soul of Darkeater Midir",
            "RC: Spears of the Church - hidden boss drop",
        ],
    ),
    DS3BossInfo(
        "Slave Knight Gael 1", "Ringed City End", 5110801, None,
        dlc = True,
        locations = [
            "RC: Soul of Slave Knight Gael",
            "RC: Blood of the Dark Soul - end boss drop",
            # These are accessible before you trigger the boss, but once you do you
            # have to beat it before getting them.
            "RC: Titanite Slab - ashes, mob drop",
            "RC: Titanite Slab - ashes, NPC drop",
            "RC: Sacred Chime of Filianore - ashes, NPC drop",
            "RC: Crucifix of the Mad King - ashes, NPC drop",
            "RC: Shira's Crown - Shira's room after killing ashes NPC",
            "RC: Shira's Armor - Shira's room after killing ashes NPC",
            "RC: Shira's Gloves - Shira's room after killing ashes NPC",
            "RC: Shira's Trousers - Shira's room after killing ashes NPC",
        ],
    ),
    DS3BossInfo(
        "Slave Knight Gael 2", "Ringed City End", 5110800, 15110800,
        dlc = True, locations = [
            "RC: Soul of Slave Knight Gael",
            "RC: Blood of the Dark Soul - end boss drop",
            # These are accessible before you trigger the boss, but once you do you
            # have to beat it before getting them.
            "RC: Titanite Slab - ashes, mob drop",
            "RC: Titanite Slab - ashes, NPC drop",
            "RC: Sacred Chime of Filianore - ashes, NPC drop",
            "RC: Crucifix of the Mad King - ashes, NPC drop",
            "RC: Shira's Crown - Shira's room after killing ashes NPC",
            "RC: Shira's Armor - Shira's room after killing ashes NPC",
            "RC: Shira's Gloves - Shira's room after killing ashes NPC",
            "RC: Shira's Trousers - Shira's room after killing ashes NPC",
        ],
    ),
    DS3BossInfo(
        "Lords of Cinder", "Kiln of the First Flame", 4100800, 14100800,
        locations = [
            "KFF: Soul of the Lords",
            "FS: Firelink Helm - shop after beating KFF boss",
            "FS: Firelink Armor - shop after beating KFF boss",
            "FS: Firelink Gauntlets - shop after beating KFF boss",
            "FS: Firelink Leggings - shop after beating KFF boss",
            "FS: Billed Mask - shop after killing Yuria",
            "FS: Black Dress - shop after killing Yuria",
            "FS: Black Gauntlets - shop after killing Yuria",
            "FS: Black Leggings - shop after killing Yuria"
        ],
    ),
]

default_yhorm_location = next(boss for boss in all_bosses if boss.name == "Yhorm the Giant")
