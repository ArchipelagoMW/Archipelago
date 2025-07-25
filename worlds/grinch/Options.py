from dataclasses import dataclass

from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionList, \
    PerGameCommonOptions


class ProgressiveVacuum(DefaultOnToggle):
    """
    Determines whether you get access to main areas progressively
    Default: Whoville > Who Forest > Who Dump > Who Lake
    """
    display_name = "Progressive Vacuum Access"

# class StartingArea(Choice):
#     """
#     Here, you can select which area you'll start the game with. Whichever one you pick is the region you'll have access to at the start of the Multiworld.
#     """
#     option_whoville = 0
#     option_who_forest = 1
#     option_who_dump = 2
#     option_who_lake = 3
#     display_name = "Starting Area"

# class Supadow(Toggle):
#     """Enables completing minigames through the Supadows in Mount Crumpit as checks. (9 locations)"""
#     display_name = "Supadow Minigame Locations"#


# class Gifts(Toggle):
#     """Missions that require you to squash every present in a level. (4 locations)"""
#     display_name = "Gift Collection Locations"


# class Movesanity(Toggle):
#     """Randomizes Grinch's moveset along with randomizing max into the pool. (Currently randomizes Max)"""
#     display_name = "Movesanity"


class UnlimitedRottenEggs(Toggle):
    """Determine whether or not you run out of rotten eggs when you utilize your gadgets."""
    display_name = "Unlimited Rotten Eggs"

@dataclass
class GrinchOptions(PerGameCommonOptions):#DeathLinkMixin
    progressive_vacuum: ProgressiveVacuum
    unlimited_rotten_eggs: UnlimitedRottenEggs