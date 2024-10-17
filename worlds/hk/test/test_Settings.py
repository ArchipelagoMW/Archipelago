from . import HKTestBase, selectSeedHK


class TestGoal_any(HKTestBase):
    options = {
        "Goal": "any",
    }


class TestGoal_hollowknight(HKTestBase):
    options = {
        "Goal": "hollowknight",
    }


class TestGoal_siblings(HKTestBase):
    options = {
        "Goal": "siblings",
    }


class TestGoal_radiance(HKTestBase):
    options = {
        "Goal": "radiance",
    }


class TestGoal_godhome(HKTestBase):
    options = {
        "Goal": "godhome",
    }


class TestGoal_godhome_flower(HKTestBase):
    options = {
        "Goal": "godhome_flower",
    }


class TestRandomize_All(HKTestBase):
    options = {
        "Goal": "any",

        "RandomizeDreamers": True,
        "RandomizeSkills": True,
        "RandomizeFocus": True,
        "RandomizeSwim": True,
        "RandomizeCharms": True,
        "RandomizeKeys": True,
        "RandomizeMaskShards": True,
        "RandomizeVesselFragments": True,
        "RandomizeCharmNotches": True,
        "RandomizePaleOre": True,
        "RandomizeGeoChests": True,
        "RandomizeJunkPitChests": True,
        "RandomizeRancidEggs": True,
        "RandomizeRelics": True,
        "RandomizeWhisperingRoots": True,
        "RandomizeBossEssence": True,
        "RandomizeGrubs": True,
        "RandomizeMimics": True,
        "RandomizeMaps": True,
        "RandomizeStags": True,
        "RandomizeLifebloodCocoons": True,
        "RandomizeGrimmkinFlames": True,
        "RandomizeJournalEntries": True,
        "RandomizeNail": True,
        "RandomizeGeoRocks": True,
        "RandomizeBossGeo": True,
        "RandomizeSoulTotems": True,
        "RandomizeLoreTablets": True,
        "RandomizeElevatorPass": True,
    }


class TestRandomize_None(HKTestBase):
    options = {
        "Goal": "any",

        "RandomizeDreamers": False,
        "RandomizeSkills": False,
        "RandomizeFocus": False,
        "RandomizeSwim": False,
        "RandomizeCharms": False,
        "RandomizeKeys": False,
        "RandomizeMaskShards": False,
        "RandomizeVesselFragments": False,
        "RandomizeCharmNotches": False,
        "RandomizePaleOre": False,
        "RandomizeGeoChests": False,
        "RandomizeJunkPitChests": False,
        "RandomizeRancidEggs": False,
        "RandomizeRelics": False,
        "RandomizeWhisperingRoots": False,
        "RandomizeBossEssence": False,
        "RandomizeGrubs": False,
        "RandomizeMimics": False,
        "RandomizeMaps": False,
        "RandomizeStags": False,
        "RandomizeLifebloodCocoons": False,
        "RandomizeGrimmkinFlames": False,
        "RandomizeJournalEntries": False,
        "RandomizeNail": False,
        "RandomizeGeoRocks": False,
        "RandomizeBossGeo": False,
        "RandomizeSoulTotems": False,
        "RandomizeLoreTablets": False,
        "RandomizeElevatorPass": False,
    }


class TestSplit_All(HKTestBase):
    options = {
        "Goal": "any",

        "SplitCrystalHeart": True,
        "SplitMothwingCloak": True,
        "SplitMantisClaw": True,
    }


class TestCosts_All(HKTestBase):
    options = {
        "Goal": "any",

        "EggShopSlots": 9,
        "SlyShopSlots": 9,
        "SlyKeyShopSlots": 9,
        "IseldaShopSlots": 9,
        "SalubraShopSlots": 9,
        "SalubraCharmShopSlots": 9,
        "LegEaterShopSlots": 9,
        "GrubfatherRewardSlots": 9,
        "SeerRewardSlots": 9,
        "ExtraShopSlots": 9,
        "CostSanity": True,
        "CostSanityHybridChance": 1,
        "CostSanityEggWeight": 1,
        "CostSanityGrubWeight": 1,
        "CostSanityEssenceWeight": 1,
        "CostSanityCharmWeight": 1,
        "CostSanityGeoWeight": 1,
    }

# RandomizeDreamers,
# RandomizeSkills,
# RandomizeFocus,
# RandomizeSwim,
# RandomizeCharms,
# RandomizeKeys,
# RandomizeMaskShards,
# RandomizeVesselFragments,
# RandomizeCharmNotches,
# RandomizePaleOre,
# RandomizeGeoChests,
# RandomizeJunkPitChests,
# RandomizeRancidEggs,
# RandomizeRelics,
# RandomizeWhisperingRoots,
# RandomizeBossEssence,
# RandomizeGrubs,
# RandomizeMimics,
# RandomizeMaps,
# RandomizeStags,
# RandomizeLifebloodCocoons,
# RandomizeGrimmkinFlames,
# RandomizeJournalEntries,
# RandomizeNail,
# RandomizeGeoRocks,
# RandomizeBossGeo,
# RandomizeSoulTotems,
# RandomizeLoreTablets,
# RandomizeElevatorPass,
# StartLocation,
# Goal,
# WhitePalace,
# SplitCrystalHeart,
# SplitMothwingCloak,
# SplitMantisClaw,
# AddUnshuffledLocations,


# # not useful without more asserts
# PreciseMovement,
# ProficientCombat,
# BackgroundObjectPogos,
# EnemyPogos,
# ObscureSkips,
# ShadeSkips,
# InfectionSkips,
# FireballSkips,
# SpikeTunnels,
# AcidSkips,
# DamageBoosts,
# DangerousSkips,
# DarkRooms,
# ComplexSkips,
# DifficultSkips,
# RemoveSpellUpgrades,
# MinimumGeoPrice,
# MaximumGeoPrice,
# MinimumGrubPrice,
# MaximumGrubPrice,
# MinimumEssencePrice,
# MaximumEssencePrice,
# MinimumCharmPrice,
# MaximumCharmPrice,
# RandomCharmCosts,
# PlandoCharmCosts,
# MinimumEggPrice,
# MaximumEggPrice,
# EggShopSlots,
# SlyShopSlots,
# SlyKeyShopSlots,
# IseldaShopSlots,
# SalubraShopSlots,
# SalubraCharmShopSlots,
# LegEaterShopSlots,
# GrubfatherRewardSlots,
# SeerRewardSlots,
# ExtraShopSlots,
# CostSanity,
# CostSanityHybridChance,
# CostSanityEggWeight,
# CostSanityGrubWeight,
# CostSanityEssenceWeight,
# CostSanityCharmWeight,
# CostSanityGeoWeight,

# # should be ok not testing
# StartingGeo,
# DeathLink,
# DeathLinkShade,
# DeathLinkBreaksFragileCharms,
# ExtraPlatforms,
