from typing import Union

from settings import Group, Bool


class StardewSettings(Group):

    class AllowAllsanityGoal(Bool):
        """Allow players to pick the goal 'Allsanity'. If disallowed, generation will fail."""

    class AllowPerfectionGoal(Bool):
        """Allow players to pick the goal 'Perfection'. If disallowed, generation will fail."""

    class AllowMaxPriceBundles(Bool):
        """Allow players to pick the option 'Bundle Price: Maximum'. If disallowed, it will be replaced with 'Very Expensive'"""

    class AllowChaosER(Bool):
        """Allow players to pick the option 'Entrance Randomizer Behavior: Chaos'. If disallowed, it will be turned off"""

    class AllowDecoupledER(Bool):
        """Allow players to pick the option 'Entrance Randomizer Behavior: Decoupled'. If disallowed, it will be turned off"""

    class AllowOverworldER(Bool):
        """Allow players to pick the option 'Entrance Randomization: Overworld or Everywhere'. If disallowed, it will be replaced with 'Buildings'"""

    class AllowShipsanityEverything(Bool):
        """Allow players to pick the option 'Shipsanity: Everything'. If disallowed, it will be replaced with 'Full Shipment With Fish'"""

    class AllowHatsanityNearOrPostPerfection(Bool):
        """Allow players to pick the option 'Hatsanity: Near Perfection OR Post Perfection'. If disallowed, it will be replaced with 'Difficult'"""

    class AllowSecretsanityDifficult(Bool):
        """Allow players to pick the option 'Secretsanity: Difficult'. If disallowed, it will be removed"""

    class AllowHellAndNightmareTraps(Bool):
        """Allow players to pick the option 'Trap Difficulty: Hell OR Nightmare'. If disallowed, it will be reduced to 'Hard'"""

    class AllowEldritchTraps(Bool):
        """Allow players to pick the option 'Trap Difficulty: Eldritch'. If disallowed, it will be reduced to 'Hard'"""

    class AllowCustomLogic(Bool):
        """Allow players to toggle on Custom logic flags. If disallowed, all flags will be disabled"""

    class AllowDataRandomization(Bool):
        """Allow players to toggle on Data Randomization flags. If disallowed, all flags will be disabled"""

    class AllowUnbalancedDataRandomizationBehavior(Bool):
        """Allow players to toggle pick Data Randomization Behaviors 'Randomized' and above. If disallowed, it will be replaced with `Weighted Randomized`"""

    class AllowJojapocalypse(Bool):
        """Allow players to enable Jojapocalypse. If disallowed, it will be disabled"""

    # class AllowSVE(Bool):
    #     """Allow players to include the mod 'Stardew Valley Expanded'. If disallowed, it will be removed from the mods"""

    allow_allsanity: Union[AllowAllsanityGoal, bool] = True
    allow_perfection: Union[AllowPerfectionGoal, bool] = True
    allow_max_bundles: Union[AllowMaxPriceBundles, bool] = True
    allow_chaos_er: Union[AllowChaosER, bool] = False
    allow_decoupled_er: Union[AllowDecoupledER, bool] = False
    allow_overworld_er: Union[AllowOverworldER, bool] = True
    allow_shipsanity_everything: Union[AllowShipsanityEverything, bool] = True
    allow_hatsanity_perfection: Union[AllowHatsanityNearOrPostPerfection, bool] = True
    allow_secretsanity_difficult: Union[AllowSecretsanityDifficult, bool] = True
    allow_hell_and_nightmare_traps: Union[AllowHellAndNightmareTraps, bool] = True
    allow_eldritch_traps: Union[AllowEldritchTraps, bool] = False
    allow_custom_logic: Union[AllowCustomLogic, bool] = True
    allow_data_randomization: Union[AllowDataRandomization, bool] = True
    allow_unbalanced_data_randomization_behavior: Union[AllowUnbalancedDataRandomizationBehavior, bool] = False
    allow_jojapocalypse: Union[AllowJojapocalypse, bool] = False
    # allow_sve: Union[AllowSVE, bool] = True
