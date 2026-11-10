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
        """Allow players to pick the option 'Entrance Randomization: Chaos'. If disallowed, it will be replaced with 'Buildings'"""

    class AllowShipsanityEverything(Bool):
        """Allow players to pick the option 'Shipsanity: Everything'. If disallowed, it will be replaced with 'Full Shipment With Fish'"""

    class AllowHatsanityNearOrPostPerfection(Bool):
        """Allow players to pick the option 'Hatsanity: Near Perfection OR Post Perfection'. If disallowed, it will be replaced with 'Difficult'"""

    class AllowCustomLogic(Bool):
        """Allow players to toggle on Custom logic flags. If disallowed, it will be disabled"""

    class AllowJojapocalypse(Bool):
        """Allow players to enable Jojapocalypse. If disallowed, it will be disabled"""

    # class AllowSVE(Bool):
    #     """Allow players to include the mod 'Stardew Valley Expanded'. If disallowed, it will be removed from the mods"""

    allow_allsanity: Union[AllowAllsanityGoal, bool] = True
    allow_perfection: Union[AllowPerfectionGoal, bool] = True
    allow_max_bundles: Union[AllowMaxPriceBundles, bool] = True
    allow_chaos_er: Union[AllowChaosER, bool] = False
    allow_shipsanity_everything: Union[AllowShipsanityEverything, bool] = True
    allow_hatsanity_perfection: Union[AllowHatsanityNearOrPostPerfection, bool] = True
    allow_custom_logic: Union[AllowCustomLogic, bool] = True
    allow_jojapocalypse: Union[AllowJojapocalypse, bool] = False
    # allow_sve: Union[AllowSVE, bool] = True
