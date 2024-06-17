from itertools import accumulate
from typing import Dict

from .ItemUtils import repeated_item_names_gen
from .Names import ItemName

# Items in PsychoRando order with the count that can be placed into the Psychonauts world before placing the items as AP
# placeholder item instead. The order and counts must exactly match ShuffleItems.lua in PsychoRando, so that the IDs
# will match.
# Used to map locally placed AP items to PsychoRando item IDs.
PSYCHORANDO_ITEM_TABLE = {
    # Current Props from AS, 6 total
    ItemName.LungfishCall: 1,
    ItemName.GloriasTrophy: 1,
    ItemName.StraightJacket: 1,
    ItemName.LobotoPainting: 1,
    ItemName.Cake: 1,
    ItemName.LilisBracelet: 1,

    # Current Props from MM, 6 total
    ItemName.StopSign: 1,
    ItemName.Flowers: 1,
    ItemName.Plunger: 1,
    ItemName.HedgeTrimmers: 1,
    ItemName.RollingPin: 1,
    ItemName.WaterCan: 1,

    # Current Props from TH, 3 total
    ItemName.Candle: 2,
    ItemName.Megaphone: 1,

    # Props from WW, 3 total
    ItemName.FredsLetter: 1,
    ItemName.PricelessCoin: 1,
    ItemName.Musket: 1,

    # 19 Psi Powers, some different names to match class
    ItemName.Marksmanship: 3,
    ItemName.Pyrokinesis: 2,
    ItemName.Confusion: 2,
    ItemName.Levitation: 3,
    ItemName.Telekinesis: 2,
    ItemName.Invisibility: 2,
    ItemName.Clairvoyance: 2,
    ItemName.Shield: 3,

    # Super Palm Bomb
    ItemName.SuperPalmBomb: 1,

    # 6 Max Ammo Up
    ItemName.AmmoUp: 6,

    # 6 Max Lives Up
    ItemName.MaxLivesUp: 6,

    # 4 Confusion Ammo Up
    ItemName.ConfusionUp: 4,

    # 10 Challenge Markers
    ItemName.ChallengeMarker: 10,

    # 19 Brain Jars, Unique Names
    ItemName.BrainJarElton: 1,
    ItemName.BrainJarBobby: 1,
    ItemName.BrainJarDogen: 1,
    ItemName.BrainJarBenny: 1,
    ItemName.BrainJarElka: 1,
    ItemName.BrainJarKitty: 1,
    ItemName.BrainJarChloe: 1,
    ItemName.BrainJarFranke: 1,
    ItemName.BrainJarJT: 1,
    ItemName.BrainJarQuentin: 1,
    ItemName.BrainJarVernon: 1,
    ItemName.BrainJarMilka: 1,
    ItemName.BrainJarCrystal: 1,
    ItemName.BrainJarClem: 1,
    ItemName.BrainJarNils: 1,
    ItemName.BrainJarMaloof: 1,
    ItemName.BrainJarMikhail: 1,
    ItemName.BrainJarPhoebe: 1,
    ItemName.BrainJarChops: 1,

    # 16 Scavenger Hunt Items, Unique Names
    ItemName.GoldDoubloon: 1,
    ItemName.EagleClaw: 1,
    ItemName.DiversHelmet: 1,
    ItemName.PsyComic: 1,
    ItemName.WoodPipe: 1,
    ItemName.TurkeySandwich: 1,
    ItemName.VoodooDoll: 1,
    ItemName.MinerSkull: 1,
    ItemName.PirateScope: 1,
    ItemName.GoldenAcorn: 1,
    ItemName.GlassEye: 1,
    ItemName.Egg: 1,
    ItemName.FertilityIdol: 1,
    ItemName.DinosaurBone: 1,
    ItemName.Fossil: 1,
    ItemName.GoldWatch: 1,

    # 50 Emotional Baggage Tags, 10 of each Type
    ItemName.SuitcaseTag: 10,
    ItemName.PurseTag: 10,
    ItemName.HatboxTag: 10,
    ItemName.SteamerTag: 10,
    ItemName.DuffleTag: 10,

    # 50 Emotional Baggage, 10 of each Type
    ItemName.Suitcase: 10,
    ItemName.Purse: 10,
    ItemName.Hatbox: 10,
    ItemName.Steamertrunk: 10,
    ItemName.Dufflebag: 10,

    # 19 Vaults
    ItemName.Vault: 19,

    # 59 Rando Arrowhead Bundles Small
    # 30 are used by default
    # 29 are added for Deep Arrowhead Shuffle
    ItemName.AHSmall: 30 + 29,

    # 25 Rando Arrowhead Bundles Large
    # 5 are used by default
    # 20 are added for Deep Arrowhead Shuffle
    ItemName.AHLarge: 5 + 20,

    # Oarsman's Badge
    ItemName.OarsmansBadge: 1,

    # Sasha's Button
    ItemName.SashaButton: 1,

    # Crow Feather
    ItemName.Feather: 1,

    # Cobweb Duster
    ItemName.CobwebDuster: 1,

    # Squirrel Dinner
    ItemName.SquirrelDinner: 1,

    # 9 Mind Unlocks
    ItemName.CoachMind: 1,
    ItemName.SashaMind: 1,
    ItemName.MillaMind: 1,
    ItemName.LindaMind: 1,
    ItemName.BoydMind: 1,
    ItemName.GloriaMind: 1,
    ItemName.FredMind: 1,
    ItemName.EdgarMind: 1,
    ItemName.OlyMind: 1,

    # Dowsing Rod
    ItemName.DowsingRod: 1,

    # 110 Psicards, filler item, increase if adding more positions
    # 54 are added for Cobweb Shuffle
    ItemName.PsiCard: 110 + 54,

    # AP Placeholders, 318 total.
    # These have no corresponding AP item and are assumed to always be last in PsychoRando's item order.
    # AP Placeholders are used to represent items from other worlds and to place local items when PsychoRando has run
    # out of IDs to place more of that local item in the game world. It is assumed that there is always enough AP
    # Placeholder items for every location in Psychonauts that can display an item in the game world.
}

# The first PsychoRando item ID for each item, calculated through a running total of the item counts.
PSYCHORANDO_BASE_ITEM_IDS: Dict[str, int] = dict(zip(
    PSYCHORANDO_ITEM_TABLE.keys(), accumulate(PSYCHORANDO_ITEM_TABLE.values(), initial=1)
))

# The maximum PsychoRando item ID, taking into account that there are multiple of some items.
MAX_PSY_ITEM_ID = sum(PSYCHORANDO_ITEM_TABLE.values())

# Lookup to get item names from PsychoRando item IDs.
PSYCHORANDO_ITEM_LOOKUP = dict(enumerate(repeated_item_names_gen(PSYCHORANDO_ITEM_TABLE, PSYCHORANDO_ITEM_TABLE),
                                         start=1))
