from typing import Dict, Set

from BaseClasses import ItemClassification

from .Names import ItemName
from .PsychoRandoItems import PSYCHORANDO_ITEM_TABLE

# Offset added to Psychonauts IDs to produce AP IDs.
AP_ITEM_OFFSET = 42690000

PROPS: Dict[str, int] = {
    ItemName.LungfishCall: 1,
    ItemName.GloriasTrophy: 2,
    ItemName.StraightJacket: 3,
    ItemName.LobotoPainting: 4,
    ItemName.Cake: 5,
    ItemName.LilisBracelet: 6,
    ItemName.OarsmansBadge: 7,
    ItemName.CobwebDuster: 9,
    ItemName.SquirrelDinner: 10,

    # The Milkman Conspiracy
    ItemName.StopSign: 11,
    ItemName.Flowers: 12,
    ItemName.Plunger: 13,
    ItemName.HedgeTrimmers: 14,
    ItemName.RollingPin: 15,

    # Gloria's Theater
    ItemName.Candle: 16,
    ItemName.Megaphone: 17,

    # Waterloo World
    ItemName.FredsLetter: 18,
    ItemName.PricelessCoin: 19,
    ItemName.Musket: 20,

    # Enabled with DeepArrowheadShuffle, otherwise available from the Main Lodge store as normal
    ItemName.DowsingRod: 93,
}

MINDS: Dict[str, int] = {
    ItemName.SashaButton: 8,
    ItemName.CoachMind: 21,
    ItemName.SashaMind: 22,
    ItemName.MillaMind: 23,
    ItemName.LindaMind: 24,
    ItemName.BoydMind: 25,
    ItemName.GloriaMind: 26,
    ItemName.FredMind: 27,
    ItemName.EdgarMind: 28,
    ItemName.OlyMind: 29,
}

PSI_POWERS: Dict[str, int] = {
    ItemName.Marksmanship: 30,
    ItemName.Pyrokinesis: 31,
    ItemName.Confusion: 32,
    ItemName.Levitation: 33,
    ItemName.Telekinesis: 34,
    ItemName.Invisibility: 35,
    ItemName.Clairvoyance: 36,
    ItemName.Shield: 37,
}

GENERAL_ITEMS: Dict[str, int] = {
    ItemName.AmmoUp: 38,
    ItemName.MaxLivesUp: 39,
    ItemName.ConfusionUp: 40,
    ItemName.ChallengeMarker: 41,
    ItemName.Vault: 42,
    ItemName.AHSmall: 43,
    ItemName.AHLarge: 44,
    ItemName.PsiCard: 45,
    ItemName.PalmMegabomb: 94,
}

BRAIN_JARS: Dict[str, int] = {
    ItemName.BrainJarElton: 46,
    ItemName.BrainJarBobby: 47,
    ItemName.BrainJarDogen: 48,
    ItemName.BrainJarBenny: 49,
    ItemName.BrainJarElka: 50,
    ItemName.BrainJarKitty: 51,
    ItemName.BrainJarChloe: 52,
    ItemName.BrainJarFranke: 53,
    ItemName.BrainJarJT: 54,
    ItemName.BrainJarQuentin: 55,
    ItemName.BrainJarVernon: 56,
    ItemName.BrainJarMilka: 57,
    ItemName.BrainJarCrystal: 58,
    ItemName.BrainJarClem: 59,
    ItemName.BrainJarNils: 60,
    ItemName.BrainJarMaloof: 61,
    ItemName.BrainJarMikhail: 62,
    ItemName.BrainJarPhoebe: 63,
    ItemName.BrainJarChops: 64,
}

SCAVENGER_HUNT_ITEMS: Dict[str, int] = {
    ItemName.GoldDoubloon: 65,
    ItemName.EagleClaw: 66,
    ItemName.DiversHelmet: 67,
    ItemName.PsyComic: 68,
    ItemName.WoodPipe: 69,
    ItemName.TurkeySandwich: 70,
    ItemName.VoodooDoll: 71,
    ItemName.MinerSkull: 72,
    ItemName.PirateScope: 73,
    ItemName.GoldenAcorn: 74,
    ItemName.GlassEye: 75,
    ItemName.Egg: 76,
    ItemName.FertilityIdol: 77,
    ItemName.DinosaurBone: 78,
    ItemName.Fossil: 79,
    ItemName.GoldWatch: 80,
}

BAGGAGE_TAGS: Dict[str, int] = {
    ItemName.SuitcaseTag: 81,
    ItemName.PurseTag: 82,
    ItemName.HatboxTag: 83,
    ItemName.SteamerTag: 84,
    ItemName.DuffleTag: 85,
}

BAGGAGE: Dict[str, int] = {
    ItemName.Suitcase: 86,
    ItemName.Purse: 87,
    ItemName.Hatbox: 88,
    ItemName.Steamertrunk: 89,
    ItemName.Dufflebag: 90,
}

OTHER_ITEMS: Dict[str, int] = {
    ItemName.Feather: 91,
    ItemName.WaterCan: 92,
}

ITEM_DICTIONARY: Dict[str, int] = {
    **PROPS,
    **MINDS,
    **PSI_POWERS,
    **BRAIN_JARS,
    **SCAVENGER_HUNT_ITEMS,
    **BAGGAGE_TAGS,
    **BAGGAGE,
    **GENERAL_ITEMS,
    **OTHER_ITEMS,
}
# Assert that there are no gaps in the item IDs
assert max(ITEM_DICTIONARY.values()) == len(ITEM_DICTIONARY), "There should not be gaps in the AP item IDs"

# Reverse mapping of all items, from item ID to item name.
REVERSE_ITEM_DICTIONARY: Dict[int, str] = {v: k for k, v in ITEM_DICTIONARY.items()}

PROGRESSION_SET: Set[str] = {
    *PROPS,
    *MINDS,
    *PSI_POWERS,
}

# Items in the PROGRESSION_SET that should be skipped during progression balancing.
SKIP_BALANCING_SET: Set[str] = {
    ItemName.HedgeTrimmers,  # Required to access 3 locations
    ItemName.RollingPin,  # Required to access 1 location
    ItemName.FredsLetter,  # Required to access 4 locations
    ItemName.PricelessCoin,  # Required to access 3 locations
    ItemName.Musket,  # Required to access 2 locations
    ItemName.Confusion,  # Required to access 2 locations
    ItemName.Cake,  # Only required for the Brain Tank goal
}

USEFUL_SET: Set[str] = {
    ItemName.Vault,
    ItemName.ChallengeMarker,
    ItemName.MaxLivesUp,
    *SCAVENGER_HUNT_ITEMS,
    *BAGGAGE_TAGS,
    *BAGGAGE,
    ItemName.AHLarge,
    ItemName.PalmMegabomb,
}

LOCAL_SET: Set[str] = {
    # Baggage must be local only
    *BAGGAGE,
}

ITEM_GROUPS: Dict[str, Set[str]] = {
    "Mind": set(MINDS.keys()),
    "Brain": set(BRAIN_JARS.keys()),
    "Scavenger Hunt": set(SCAVENGER_HUNT_ITEMS.keys()),
}

# Skip creating the set if assertions are disabled.
if __debug__:
    # Every AP item must be present in PsychoRando, but not necessarily the other way around.
    _items_not_in_psychorando = set(ITEM_DICTIONARY).difference(PSYCHORANDO_ITEM_TABLE)
    assert not _items_not_in_psychorando, f"Some AP items are not present in PsychoRando: {_items_not_in_psychorando}"
    del _items_not_in_psychorando

# The number of each AP item in the item pool, typically matching the maximum number of each item that can be placed
# into the Psychonauts game world.
ITEM_COUNT: Dict[str, int] = {
    **PSYCHORANDO_ITEM_TABLE,
    # Automatically added as filler items, so none are added to the item pool directly.
    ItemName.PsiCard: 0,
    **{item: 0 for item in OTHER_ITEMS},
    # Only added when DeepArrowheadShuffle is enabled.
    ItemName.DowsingRod: 0,
    # The extra available Arrowhead Bundles are only used when DeepArrowheadShuffle is enabled.
    ItemName.AHSmall: 30,
    ItemName.AHLarge: 5,
}

# Classification for each item. Items not in the Dict are assumed to be Filler.
BASE_ITEM_CLASSIFICATIONS: Dict[str, ItemClassification] = {}
for item_name in PROGRESSION_SET:
    if item_name in SKIP_BALANCING_SET:
        BASE_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression_skip_balancing
    else:
        BASE_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.progression
for item_name in USEFUL_SET:
    BASE_ITEM_CLASSIFICATIONS[item_name] = ItemClassification.useful

# Items where only the first copy is progression balanced.
# Only one of each PSI Power is progression balanced because there are no locations that require an
# upgraded PSI Power to access.
# Only the first Candle is progression balanced because the second candle is only required to access a single
# location.
SKIP_BALANCING_FOR_DUPLICATES: Set[str] = {
    *PSI_POWERS,
    ItemName.Candle,
}
