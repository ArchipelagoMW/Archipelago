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

class ShuffleLostGestrals(Toggle):
    """
    Shuffles the lost gestrals into the item pool.
    """
    internal_name = "shuffle_lost_gestrals"
    display_name = "Shuffle Lost Gestrals"

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
    display_name = "Area logic"
    option_normal = 0
    option_hard = 1
    option_no_logic = 2
    default = 0

class ShuffleCharacters(Toggle):
    """Shuffles characters into the item pool."""
    display_name = "Shuffle characters"

class StartingCharacter(Choice):
    """Determines which character you start with. Does nothing if Shuffle Characters is set to false."""
    internal_name = "starting_character"
    display_name = "Starting character"
    option_gustave = 0
    option_lune = 1
    option_maelle = 2
    option_sciel = 3
    option_monoco = 4
    default = 0

class ClairObscurStartInventory(StartInventory):
    """
    Start with these items
    """

@dataclass
class ClairObscurOptions(PerGameCommonOptions):
    goal: Goal
    char_shuffle: ShuffleCharacters
    gestral_shuffle: ShuffleLostGestrals
    starting_char: StartingCharacter

    start_inventory: ClairObscurStartInventory

OPTIONS_GROUP = [
    OptionGroup(
        "Item & Location Options", [
            ClairObscurStartInventory,
        ], False,
    ),
]