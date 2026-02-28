"""Test file used for checking total coins available for each kong."""

import randomizer.CollectibleLogicFiles.AngryAztec as AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle as CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves as CrystalCaves
import randomizer.CollectibleLogicFiles.DKIsles as DKIsles
import randomizer.CollectibleLogicFiles.FranticFactory as FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest as FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon as GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes as JungleJapes
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs


def __CountCoinsForRegion(coinTotals, collectibles):
    for collectible in collectibles:
        if collectible.type == Collectibles.coin:
            if collectible.kong in coinTotals:
                coinTotals[collectible.kong] += collectible.amount


coinTotals = {Kongs.donkey: 0, Kongs.diddy: 0, Kongs.lanky: 0, Kongs.tiny: 0, Kongs.chunky: 0}

print("Counting coins across all levels...\n")

for region, collectibles in JungleJapes.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in AngryAztec.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in FranticFactory.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in GloomyGalleon.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in FungiForest.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in CrystalCaves.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in CreepyCastle.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

for region, collectibles in DKIsles.LogicRegions.items():
    __CountCoinsForRegion(coinTotals, collectibles)

print("Total Coins Per Kong:")
print("=" * 40)
for kong, total in coinTotals.items():
    print(f"{kong.name}: {total + 80}")

print("Done.")
