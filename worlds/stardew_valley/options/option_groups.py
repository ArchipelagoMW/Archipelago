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
            options.FriendsanityHeartSize,
            options.Monstersanity,
            options.Shipsanity,
            options.Cooksanity,
            options.Chefsanity,
            options.Craftsanity,
            options.Booksanity,
            options.Walnutsanity,
        ]),
        OptionGroup("Multipliers and Buffs", [
            options.StartingMoney,
            options.ProfitMargin,
            options.ExperienceMultiplier,
            options.FriendshipMultiplier,
            options.DebrisMultiplier,
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
    ]
