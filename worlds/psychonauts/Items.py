from typing import Dict, List

from .Names import ItemName
from .PsychoRandoItems import PSYCHORANDO_ITEM_TABLE

# Offset added to Psychonauts IDs to produce AP IDs.
AP_ITEM_OFFSET = 42690000

PROPS = {
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
    ItemName.PropSign: 11,
    ItemName.PropFlowers: 12,
    ItemName.PropPlunger: 13,
    ItemName.PropHedgeTrimmers: 14,
    ItemName.PropRollingPin: 15,

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

MINDS = {
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

PSI_POWERS = {
    ItemName.Marksmanship: 30,
    ItemName.Pyrokinesis: 31,
    ItemName.Confusion: 32,
    ItemName.Levitation: 33,
    ItemName.Telekinesis: 34,
    ItemName.Invisibility: 35,
    ItemName.Clairvoyance: 36,
    ItemName.Shield: 37,
}

GENERAL_ITEMS = {
    ItemName.AmmoUp: 38,
    ItemName.MaxLivesUp: 39,
    ItemName.ConfusionUp: 40,
    ItemName.ChallengeMarker: 41,
    ItemName.Vault: 42,
    ItemName.AHSmall: 43,
    ItemName.AHLarge: 44,
    ItemName.PsiCard: 45,
    ItemName.SuperPalmBomb: 94,
}

BRAIN_JARS = {
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

SCAVENGER_HUNT_ITEMS = {
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

BAGGAGE_TAGS = {
    ItemName.SuitcaseTag: 81,
    ItemName.PurseTag: 82,
    ItemName.HatboxTag: 83,
    ItemName.SteamerTag: 84,
    ItemName.DuffleTag: 85,
}

BAGGAGE = {
    ItemName.Suitcase: 86,
    ItemName.Purse: 87,
    ItemName.Hatbox: 88,
    ItemName.Steamertrunk: 89,
    ItemName.Dufflebag: 90,
}

OTHER_ITEMS = {
    ItemName.Feather: 91,
    ItemName.PropWaterCan: 92,
}

ITEM_DICTIONARY = {
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
REVERSE_ITEM_DICTIONARY = {v: k for k, v in ITEM_DICTIONARY.items()}

PROGRESSION_SET = {
    *PROPS,
    *MINDS,
    *PSI_POWERS,
}

USEFUL_SET = {
    ItemName.Vault,
    ItemName.ChallengeMarker,
    ItemName.MaxLivesUp,
    *SCAVENGER_HUNT_ITEMS,
    *BAGGAGE_TAGS,
    *BAGGAGE,
    ItemName.AHLarge,
    ItemName.SuperPalmBomb,
}

LOCAL_SET = {
    # Baggage must be local only
    *BAGGAGE,
}

ITEM_GROUPS: Dict[str, List[str]] = {
    "Mind": list(MINDS.keys()),
    "Brain": list(BRAIN_JARS.keys()),
    "Scavenger Hunt": list(SCAVENGER_HUNT_ITEMS.keys()),
}

# Skip creating the set if assertions are disabled.
if __debug__:
    # Every AP item must be present in PsychoRando, but not necessarily the other way around.
    _items_not_in_psychorando = set(ITEM_DICTIONARY).difference(PSYCHORANDO_ITEM_TABLE)
    assert not _items_not_in_psychorando, f"Some AP items are not present in PsychoRando: {_items_not_in_psychorando}"
    del _items_not_in_psychorando

# The number of each AP item in the item pool, typically matching the maximum number of each item that can be placed
# into the Psychonauts game world.
ITEM_COUNT = {
    **PSYCHORANDO_ITEM_TABLE,
    # Automatically added as filler items, so none are added to the item pool directly.
    ItemName.PsiCard: 0,
    # These items are unused.
    **{item: 0 for item in OTHER_ITEMS},
    # Only added when DeepArrowheadShuffle is enabled.
    ItemName.DowsingRod: 0,
    # The extra available Arrowhead Bundles are only used when DeepArrowheadShuffle is enabled.
    ItemName.AHSmall: 30,
    ItemName.AHLarge: 5,
}
