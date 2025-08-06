from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventory, OptionGroup, Toggle


class Goal(Choice):
    """
    The victory condition for your run
    """

    display_name = "Goal"
    option_paintress = 0
    option_curator = 1
    option_painted_love = 2
    option_simon = 3

    default = 1

class ExcludeLocations(Choice):
    """
    This will remove all Endless Tower locations from the pool.
    None: No locations excluded.
    Endless Tower:
    """
    internal_name = "exclude_endgame_locations"
    display_name = "Exclude Endgame Locations"
    option_none = 0
    option_endless = 1
    option_drafts = 2
    option_both = 3
    default = 3

class ShuffleLostGestrals:
    internal_name = "shuffle_lost_gestrals"
    display_name = "Shuffle Lost Gestrals"
    option_false = 0
    option_gestrals = 1
    option_rewards = 2
    option_both = 3

class ClairObscurStartInventory(StartInventory):
    """
    Start with these items
    """

@dataclass
class ClairObscurOptions(PerGameCommonOptions):
    goal: Goal

    start_inventory: ClairObscurStartInventory

OPTIONS_GROUP = [
    OptionGroup(
        "Item & Location Options", [
            ClairObscurStartInventory,
        ], False,
    ),
]