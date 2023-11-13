# In almost all cases, we leave boss and enemy randomization up to the offline randomizer. But for
# Yhorm specifically we need to know where he ends up in order to ensure that the Storm Ruler is
# available before his fight.

from dataclasses import dataclass, field
from typing import Optional, Set

@dataclass
class DS3BossInfo:
    """The set of locations and regions a given boss location blocks access to."""

    name: str
    """The boss's name."""

    id: int
    """The game's ID for this particular boss."""

    dlc: bool = False
    """This boss appears in one of the game's DLCs."""

    region: Optional[str] = None
    """The name the region that can't be accessed until the boss is dead, if one exists."""

    locations: Optional[str] = field(default_factory=set)
    """Additional individual locations that can't be accessed until the boss is dead."""


# Note: the offline randomizer splits up some bosses into separate fights for separate phases, each
# of which can be individually replaced by Yhorm.
all_bosses = [
    DS3BossInfo("Iudex Gundyr", 4000800, region = "Firelink Shrine",
        locations = {"CA: Coiled Sword"}),
    DS3BossInfo("Vordt of the Boreal Valley", 3000800, region = "Undead Settlement",
        locations = {"HWL: Soul of Boreal Valley Vordt"}),
    DS3BossInfo("Curse-rotted Greatwood", 3100800, locations = {
        "US: Soul of the Rotted Greatwood",
        "US: Transposing Kiln",
        "US: Wargod Wooden Shield",
    }),
    DS3BossInfo("Crystal Sage", 3300850, region = "Cathedral of the Deep", locations = {
        "RS: Soul of a Crystal Sage",
        "RS: Sage's Big Hat",
    }),
    DS3BossInfo("Deacons of the Deep", 3500800, locations = {
        "CD: Soul of the Deacons of the Deep",
        "CD: Small Doll",
    }),
    DS3BossInfo("Abyss Watchers", 3300801, region = "Catacombs of Carthus", locations = {
        "FK: Soul of the Blood of the Wolf",
        "FK: Cinders of a Lord - Abyss Watcher",
        "UG: Hornet Ring",
        "FK: Undead Legion Helm",
        "FK: Undead Legion Armor",
        "FK: Undead Legion Gauntlet",
        "FK: Undead Legion Leggings",
        "UG: Wolf Knight Helm",
        "UG: Wolf Knight Armor",
        "UG: Wolf Knight Gauntlets",
        "UG: Wolf Knight Leggings",
    }),
    DS3BossInfo("High Lord Wolnir", 3800800, region = "Irithyll of the Boreal Valley", locations = {
        "CC: Soul of High Lord Wolnir",
        "CC: Wolnir's Crown",
        "CC: Homeward Bone",
        "CC: Pontiff's Right Eye",
    }),
    DS3BossInfo("Pontiff Sulyvahn", 3700850, region = "Anor Londo", locations = {
        "IBV: Soul of Pontiff Sulyvahn",
    }),
    DS3BossInfo("Old Demon King", 3800830, locations = {
        "SL: Soul of the Old Demon King",
    }),
    DS3BossInfo("Aldrich, Devourer of Men", 3700800, locations = {
        "AL: Soul of Aldrich",
        "AL: Cinders of a Lord - Aldrich",
        "AL: Smough's Helm",
        "AL: Smough's Armor",
        "AL: Smough's Gauntlets",
        "AL: Smough's Leggings",
        "AL: Sun Princess Ring",
    }),
    DS3BossInfo("Dancer of the Boreal Valley", 3000899, region = "Lothric Castle", locations = {
        "HWL: Soul of the Dancer",
    }),
    DS3BossInfo("Dragonslayer Armour", 3010800, region = "Grand Archives", locations = {
        "LC: Soul of Dragonslayer Armour",
        "LC: Morne's Helm",
        "LC: Morne's Armor",
        "LC: Morne's Gauntlets",
        "LC: Morne's Leggings",
        "LC: Titanite Chunk #11",
    }),
    DS3BossInfo("Consumed King Oceiros", 3000830, region = "Untended Graves", locations = {
        "CKG: Soul of Consumed Oceiros",
        "CKG: Titanite Scale #2",
        "CKG: Titanite Scale #3",
    }),
    DS3BossInfo("Champion Gundyr", 4000830, locations = {
        "UG: Soul of Champion Gundyr",
        "UG: Gundyr's Helm",
        "UG: Gundyr's Armor",
        "UG: Gundyr's Gauntlets",
        "UG: Gundyr's Leggings",
        "UG: Hornet Ring",
        "UG: Chaos Blade",
        "UG: Blacksmith Hammer",
        "UG: Eyes of a Fire Keeper",
        "UG: Coiled Sword Fragment",
        "UG: Soul of a Crestfallen Knight #2",
        "UG: Life Ring+3",
        "UG: Ring of Steel Protection+1",
        "UG: Ring of Sacrifice",
        "UG: Ring of Sacrifice",
        "UG: Ember",
        "UG: Wolf Knight Helm",
        "UG: Wolf Knight Armor",
        "UG: Wolf Knight Gauntlets",
        "UG: Wolf Knight Leggings",
    }),
    # This is a white lie, you can get to a bunch of items in AP before you beat the Wyvern, but
    # this saves us from having to split the entire region in two just to mark which specific items
    # are before and after.
    DS3BossInfo("Ancient Wyvern", 3200800, region = "Archdragon Peak"),
    DS3BossInfo("King of the Storm", 3200850, locations = {
        "AP: Soul of the Nameless King",
        "AP: Golden Crown",
        "AP: Dragonscale Armor",
        "AP: Golden Bracelets",
        "AP: Dragonscale Waistcloth",
        "AP: Titanite Slab #2",

    }),
    DS3BossInfo("Nameless King", 3200851, locations = {
        "AP: Soul of the Nameless King",
        "AP: Golden Crown",
        "AP: Dragonscale Armor",
        "AP: Golden Bracelets",
        "AP: Dragonscale Waistcloth",
        "AP: Dragonslayer Helm",
        "AP: Dragonslayer Armor",
        "AP: Dragonslayer Gauntlets",
        "AP: Dragonslayer Leggings",
    }),
    DS3BossInfo("Lorian, Elder Prince", 3410830, locations = {
        "GA: Soul of the Twin Princes",
        "GA: Cinders of a Lord - Lothric Prince",
    }),
    DS3BossInfo("Lothric, Younger Prince", 3410832, locations = {
        "GA: Soul of the Twin Princes",
        "GA: Cinders of a Lord - Lothric Prince",
        "GA: Lorian's Helm",
        "GA: Lorian's Armor",
        "GA: Lorian's Gauntlets",
        "GA: Lorian's Leggings",
    }),
    DS3BossInfo("Champion's Gravetender and Gravetender Greatwolf", 4500860, dlc = True, locations = {
        "PW1: Valorheart",
        "PW1: Champion's Bones",
    }),
    DS3BossInfo("Sister Friede", 4500801, dlc = True, region = "Dreg Heap", locations = {
        "PW2: Soul of Sister Friede",
        "PW2: Titanite Slab (Friede)",
        "PW2: Ordained Hood",
        "PW2: Ordained Dress",
        "PW2: Ordained Trousers",
    }),
    DS3BossInfo("Blackflame Friede", 4500800, dlc = True, region = "Dreg Heap", locations = {
        "PW2: Soul of Sister Friede",
        "PW2: Ordained Hood",
        "PW2: Ordained Dress",
        "PW2: Ordained Trousers",
    }),
    DS3BossInfo("Demon Prince", 5000801, dlc = True, region = "Ringed City", locations = {
        "DH: Soul of the Demon Prince",
        "DH: Small Envoy Banner",
    }),
    DS3BossInfo("Halflight, Spear of the Church", 5100800, dlc = True, locations = {
        "RC: Titanite Slab #1",
        "RC: Titanite Slab #2",
        "RC: Titanite Slab #3",
        "RC: Filianore's Spear Ornament",
        "RC: Sacred Chime of Filianore",
        "RC: Crucifix of the Mad King",
    }),
    DS3BossInfo("Darkeater Midir", 5100850, dlc = True, locations = {
        "RC: Soul of Darkeater Midir",
        "RC: Spears of the Church",
    }),
    DS3BossInfo("Slave Knight Gael 1", 5110801, dlc = True, locations = {
        "RC: Soul of Slave Knight Gael",
        "RC: Blood of the Dark Soul",
    }),
    DS3BossInfo("Slave Knight Gael 2", 5110800, dlc = True, locations = {
        "RC: Soul of Slave Knight Gael",
        "RC: Blood of the Dark Soul",
    }),
    DS3BossInfo("Soul of Cinder", 4100800),
]

default_yhorm_location = DS3BossInfo("Yhorm the Giant", 3900800, locations = {
    "PC: Soul of Yhorm the Giant",
    "PC: Cinders of a Lord - Yhorm the Giant",
})
