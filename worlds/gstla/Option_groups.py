from Options import StartInventoryPool
from .Options import (ItemShuffle, RevealHiddenItem, OmitLocations, AddGs1Items, AddDummyItems,
                      StartWithShip, ShipWings, AnemosAccess, CharacterShuffle, SecondStartingCharacter,
                      CharStatShuffle, CharEleShuffle, NoLearningUtilPsy, RandomizeClassStatBoosts,
                      ClassPsynergy, ClassPsynergyLevels, AdjustPsyPower, AdjustPsyCost, RandomizePsyAoe,
                      AdjustEnemyPsyPower, RandomizeEnemyPsyAoe, EnemyEResShuffle, StartWithHealPsynergy,
                      StartWithRevivePsynergy, DjinnShuffle, DjinnLogic,
                      ShuffleDjinnStats, AdjustDjinnPower, RandomizeDjinnAoe, ScaleDjinnBattleDifficulty,
                      RandomizeSummonCosts, AdjustSummonPower, RandomizeEqCompatibility, AdjustEqPrices,
                      AdjustEqStats, ShuffleAttack, ShuffleWpnEffects, ShuffleDefense, ShuffleArmEffect,
                      RandomizeEqCurses, RemoveCurses, VisibleItems, FreeAvoid, FreeRetreat, ScaleExpGained,
                      ScaleCoinsGained, StartingLevels, SanctuaryReviveCost, AvoidPatch, EnableHardMode,
                      HalveEncounterRate, EasierBosses, NamedPuzzles, ManualRetreatGlitch, MusicShuffle,
                      TelportEverywhere, TrapChance, MimicTrapWeight, ForgeMaterialsFillerWeight,
                      RustyMaterialsFillerWeight, StatBoostFillerWeight, UncommonConsumableFillerWeight,
                      ForgedEquipmentFillerWeight, LuckyEquipmentFillerWeight, ShopEquipmentFillerWeight,
                      CoinsFillerWeight, CommonConsumablesFillerWeight, AutoRun, ScaleMimics, ScaleCharacters,
                      MaxScaledLevel, ForgeMaterialsAreFiller, ArtifactsAreFiller, DisableShopGameTickets,
                      Goal, RandomGoals, DjinnHuntCount, SummonHuntCount, ShortcutMarsLighthouse, ShortcutMagmaRock)

from Options import OptionGroup


gstla_option_groups = [
    OptionGroup("General Pool", [
        ItemShuffle,
        OmitLocations,
        AddGs1Items,
        AddDummyItems
    ]),
    OptionGroup("Goal", [
        Goal,
        RandomGoals,
        DjinnHuntCount,
        SummonHuntCount
    ]),
    OptionGroup("Logic Adjustments", [
        RevealHiddenItem,
        StartWithShip,
        ShipWings,
        AnemosAccess,
        DjinnLogic,
        NamedPuzzles,
        ShortcutMarsLighthouse,
        ShortcutMagmaRock
    ]),
    OptionGroup("Character Changes", [
        CharacterShuffle,
        SecondStartingCharacter,
        ScaleCharacters,
        MaxScaledLevel,
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
        MusicShuffle,
        AutoRun,
        DisableShopGameTickets,
    ]),
    OptionGroup("Trap and Filler Distribution", [
        ForgeMaterialsAreFiller,
        ArtifactsAreFiller,
        TrapChance, 
        MimicTrapWeight,
        ScaleMimics,
        ForgeMaterialsFillerWeight,
        RustyMaterialsFillerWeight,
        StatBoostFillerWeight,
        UncommonConsumableFillerWeight,
        ForgedEquipmentFillerWeight,
        LuckyEquipmentFillerWeight,
        ShopEquipmentFillerWeight,
        CoinsFillerWeight,
        CommonConsumablesFillerWeight
    ])
]