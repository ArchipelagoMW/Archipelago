import logging

import Options as ap_options
from . import options

sv_option_groups = []
try:
    from Options import OptionGroup
except ImportError:
    logging.warning("Old AP Version, OptionGroup not available.")
else:
    sv_option_groups = [
        OptionGroup("General", [
            options.Goal,
            options.FarmType,
            options.BundleRandomization,
            options.BundlePrice,
            options.BundlePerRoom,
            options.EntranceRandomization,
            options.ExcludeGingerIsland,
        ]),
        OptionGroup("Major Unlocks", [
            options.SeasonRandomization,
            options.Cropsanity,
            options.BackpackProgression,
            options.ToolProgression,
            options.ElevatorProgression,
            options.SkillProgression,
            options.BuildingProgression,
        ]),
        OptionGroup("Extra Shuffling", [
            options.FestivalLocations,
            options.ArcadeMachineLocations,
            options.SpecialOrderLocations,
            options.QuestLocations,
            options.Fishsanity,
            options.Museumsanity,
            options.Friendsanity,
            options.Monstersanity,
            options.Chefsanity,
            options.Booksanity,
            options.Walnutsanity,
            options.Moviesanity,
        ]),
        OptionGroup("Extreme Options", [
            options.Shipsanity,
            options.Cooksanity,
            options.Craftsanity,
            options.Eatsanity,
            options.Secretsanity,
            options.Hatsanity,
            options.IncludeEndgameLocations,
        ]),
        OptionGroup("Multipliers, Buffs and extra customization", [
            options.StartingMoney,
            options.ProfitMargin,
            options.ExperienceMultiplier,
            options.FriendshipMultiplier,
            options.FriendsanityHeartSize,
            options.DebrisMultiplier,
            options.BackpackSize,
            options.NumberOfMovementBuffs,
            options.EnabledFillerBuffs,
            options.TrapDifficulty,
            options.TrapDistribution,
            options.MultipleDaySleepEnabled,
            options.MultipleDaySleepCost,
            options.QuickStart,
        ]),
        OptionGroup("Advanced Options", [
            options.Gifting,
            ap_options.DeathLink,
            options.Mods,
            options.BundlePlando,
            ap_options.ProgressionBalancing,
            ap_options.Accessibility,
        ]),
        OptionGroup("Jojapocalypse", [
            options.Jojapocalypse,
            options.JojaStartPrice,
            options.JojaEndPrice,
            options.JojaPricingPattern,
            options.JojaPurchasesForMembership,
            options.JojaAreYouSure,
        ]),
    ]
