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

class ShuffleLostGestrals(Choice):
    """
    Unimplemented
    Shuffles the lost gestrals and/or their rewards into the pool as items and locations.
    """
    internal_name = "shuffle_lost_gestrals"
    display_name = "Shuffle Lost Gestrals"
    option_false = 0
    option_gestrals = 1
    option_rewards = 2
    option_both = 3

class AreaLogic(Choice):
    """
    Unimplemented
    Determines how many major area unlock items will be placed how early.
    Normal: Act 1 major areas won't be placed past Act 1; Forgotten Battlefield and Old Lumiere won't be placed behind
    Visages/Sirene; Visages and Sirene won't be placed behind The Monolith.
    Hard: Only half of the major areas will be placed in those segments.
    No Logic: Areas could be anywhere. You may need to grind world map enemies for a long time.
    """
    internal_name = "area_logic"
    display_name = "Area Logic"
    option_normal = 0
    option_hard = 1
    option_no_logic = 2
    default = 0

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