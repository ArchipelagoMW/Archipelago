from Options import StartInventoryPool
from .Options import (ItemShuffle, MajorMinorSplit, RevealHiddenItem, OmitLocations, AddGs1Items, AddDummyItems,
                      StartWithShip, ShipWings, AnemosAccess, CharacterShuffle, SecondStartingCharacter,
                      CharStatShuffle, CharEleShuffle, NoLearningUtilPsy, RandomizeClassStatBoosts,
                      ClassPsynergy, ClassPsynergyLevels, AdjustPsyPower, AdjustPsyCost, RandomizePsyAoe,
                      AdjustEnemyPsyPower, RandomizeEnemyPsyAoe, EnemyEResShuffle, StartWithHealPsynergy,
                      StartWithRevivePsynergy, StartWithRevealPsynergy, DjinnShuffle, DjinnLogic,
                      ShuffleDjinnStats, AdjustDjinnPower, RandomizeDjinnAoe, ScaleDjinnBattleDifficulty,
                      RandomizeSummonCosts, AdjustSummonPower, RandomizeEqCompatibility, AdjustEqPrices,
                      AdjustEqStats, ShuffleAttack, ShuffleWpnEffects, ShuffleDefense, ShuffleArmEffect,
                      RandomizeEqCurses, RemoveCurses, VisibleItems, FreeAvoid, FreeRetreat, ScaleExpGained,
                      ScaleCoinsGained, StartingLevels, SanctuaryReviveCost, AvoidPatch, EnableHardMode,
                      HalveEncounterRate, EasierBosses, NamedPuzzles, ManualRetreatGlitch, MusicShuffle,
                      TelportEverywhere, TrapChance, MimicTrapWeight, ForgeMaterialsFillerWeight,
                      RustyMaterialsFillerWeight, StatBoostFillerWeight, UncommonConsumableFillerWeight,
                      ForgedEquipmentFillerWeight, LuckyFountainEquipmentFillerWeight, ShopEquipmentFillerWeight,
                      CoinsFillerWeight, CommonConsumablesFillerWeight)

from Options import OptionGroup


gstla_option_groups = [
    OptionGroup("General Pool", [
        ItemShuffle,
        MajorMinorSplit,
        OmitLocations,
        AddGs1Items,
        AddDummyItems
    ]),
    OptionGroup("Logic Adjustments", [
        RevealHiddenItem,
        StartWithShip,
        ShipWings,
        AnemosAccess,
        DjinnLogic,
        NamedPuzzles
    ]),
    OptionGroup("Character Changes", [
        CharacterShuffle,
        SecondStartingCharacter,
        CharStatShuffle,
        CharEleShuffle,
        RandomizeClassStatBoosts
    ]),
    OptionGroup("Psynergy Changes", [
        NoLearningUtilPsy,
        ClassPsynergy,
        ClassPsynergyLevels,
        AdjustPsyPower,
        AdjustPsyCost,
        RandomizePsyAoe,
        AdjustEnemyPsyPower,
        RandomizeEnemyPsyAoe,
        EnemyEResShuffle,
    ]),
    OptionGroup("Djinn and Summon Changes", [
        DjinnShuffle,
        ShuffleDjinnStats,
        AdjustDjinnPower,
        RandomizeDjinnAoe,
        ScaleDjinnBattleDifficulty,
        RandomizeSummonCosts,
        AdjustSummonPower
    ]),
    OptionGroup("Equipment Changes", [
        RandomizeEqCompatibility,
        AdjustEqPrices,
        AdjustEqStats,
        ShuffleAttack,
        ShuffleWpnEffects,
        ShuffleDefense,
        ShuffleArmEffect,
        RandomizeEqCurses,
        RemoveCurses
    ]),
    OptionGroup("Quality Of Life", [
        StartWithHealPsynergy,
        StartWithRevivePsynergy,
        StartWithRevealPsynergy,
        FreeAvoid,
        AvoidPatch,
        FreeRetreat,
        ManualRetreatGlitch,
        SanctuaryReviveCost,
        EnableHardMode,
        HalveEncounterRate,
        EasierBosses,
        TelportEverywhere,
        ScaleExpGained,
        ScaleCoinsGained,
        StartingLevels,
        VisibleItems,
        MusicShuffle
    ]),
    OptionGroup("Trap and Filler Distribution", [
        TrapChance, 
        MimicTrapWeight,
        ForgeMaterialsFillerWeight,
        RustyMaterialsFillerWeight,
        StatBoostFillerWeight,
        UncommonConsumableFillerWeight,
        ForgedEquipmentFillerWeight,
        LuckyFountainEquipmentFillerWeight,
        ShopEquipmentFillerWeight,
        CoinsFillerWeight,
        CommonConsumablesFillerWeight
    ])
]