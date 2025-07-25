from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionList

class KeyType(Choice):
    """Selects whether you want your access items to be separated or progressive"""
    display_name = "Key Type"
    option_separated = 0
    option_progressive = 1
    default = 0

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
#     display_name = "Supadow Minigame Locations"
#
#
# class Gifts(Toggle):
#     """Missions that require you to squash every present in a level. (4 locations)"""
#     display_name = "Gift Collection Locations"


# class Movesanity(Toggle):
#     """Randomizes Grinch's moveset along with randomizing max into the pool. (Currently randomizes Max)"""
#     display_name = "Movesanity"


class RottenEggs(Toggle):
    """Determine whether or not you run out of rotten eggs when you utilize your gadgets."""
    display_name = "Unlimited Rotten Eggs"