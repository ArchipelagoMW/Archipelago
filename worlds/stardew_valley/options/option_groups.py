import logging
from inspect import cleandoc

import Options as ap_options
from . import options

sv_option_groups = []
try:
    from Options import OptionGroup
except ImportError:
    logging.warning("Old AP Version, OptionGroup not available.")
else:
    sv_option_groups = [
        OptionGroup(
            "General",
            [
                options.Goal,
                options.FarmType,
                options.BundleRandomization,
                options.BundlePrice,
                options.BundlePerRoom,
                options.EntranceRandomization,
                options.ExcludeGingerIsland,
            ],
            description=cleandoc(
                """
                These settings decide what your playthrough will be.
                They do not directly add or remove shuffled locations or items, but instead shape the playthrough in other ways.
                """
            )),
        OptionGroup(
            "Major Unlocks",
            [
                options.SeasonRandomization,
                options.Cropsanity,
                options.BackpackProgression,
                options.ToolProgression,
                options.ElevatorProgression,
                options.SkillProgression,
                options.BuildingProgression,
                options.StartWithout,
            ],
            description=cleandoc(
                """
                These settings are critical customization of items and locations.
                They are the biggest deciders of progression style, and how much of the core mechanics of the game will start out locked and be randomized.
                Turning off some of these settings can make the playthrough more open, and more difficult as a result.
                """
            )),
        OptionGroup(
            "Extra Shuffling",
            [
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
            ],
            description=cleandoc(
                """
                These settings will shuffle an extra game mechanic, that is not critical to the playthrough but can help fit a specific theme, or add replayability to something that is otherwise always the same.
                They generally focus on one very specific mechanic, and you decide whether to shuffle it or not, and to what extent.
                """
            )),
        OptionGroup(
            "Extreme Options",
            [
                options.Shipsanity,
                options.Cooksanity,
                options.Craftsanity,
                options.Eatsanity,
                options.Secretsanity,
                options.Hatsanity,
                options.IncludeEndgameLocations,
            ],
            description=cleandoc(
                """
                These settings work similarly to the "Extra Shuffling" settings, but have the potential to make a run extremely difficult or time-consuming.
                Recommended only for experienced players, not for the faint of heart.
                """
            )),
        OptionGroup(
            "Multipliers, Buffs and extra customization",
            [
                options.StartingMoney,
                options.ProfitMargin,
                options.ExperienceMultiplier,
                options.FriendshipMultiplier,
                options.FriendsanityHeartSize,
                options.DebrisMultiplier,
                options.BackpackSize,
                options.NumberOfMovementBuffs,
                options.EnabledFillerBuffs,
                options.AllowedFillerItems,
                options.TrapDifficulty,
                options.TrapDistribution,
                options.MultipleDaySleepEnabled,
                options.MultipleDaySleepCost,
                options.QuickStart,
            ],
            description=cleandoc(
                """
                These settings do not directly add or remove randomization, but instead serve to customize difficulty, grinding, and overall duration of the slot.
                These have direct effects on in-game behaviors, not tied to the Archipelago randomization.
                These settings are a good way to make a seed objectively easier or harder in a very predictable way.
                """
            )),
        OptionGroup(
            "Advanced Options",
            [
                options.Gifting,
                ap_options.DeathLink,
                options.Mods,
                options.BundleWhitelist,
                options.BundleBlacklist,
                options.CustomLogic,
                ap_options.ProgressionBalancing,
                ap_options.Accessibility,
            ],
            description=cleandoc(
                """
                These settings are more complicated to understand and should generally be left default.
                Intended for power users, experienced Archipelago players and hosts, and people trying to create an extremely customized run, for example for a themed event.
                """
            )),
        OptionGroup(
            "Jojapocalypse",
            [
                options.Jojapocalypse,
                options.JojaStartPrice,
                options.JojaEndPrice,
                options.JojaPricingPattern,
                options.JojaPurchasesForMembership,
                options.JojaAreYouSure,
            ],
            description=cleandoc(
                """
                Jojapocalypse is an overhaul of the progression of the randomizer, thematically equivalent to the Joja Route from the vanilla game.
                It is designed as an intnetionally unsatisfying, difficult, unfun experience, to make the player experience the consequences of encouraging Joja, and regret their choice.
                Jojapocalypse can be extremely mentally taxing and unpleasant. As a result, it can only be generated locally, not on the website, and only by having the host explicitly consent to it by modifying their `host.yaml` file to allow it.
                These settings serve to enable and customize Jojapocalypse
                """
            )),
    ]
