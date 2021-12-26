from Options import Choice, Range, Option
import typing


class StartingGender(Choice):
    """
    Determines the gender of your initial 'Sir Lee' character.
    """
    displayname = "Starting Gender"
    option_sir = 0
    option_lady = 1
    alias_male = 0
    alias_female = 1
    default = 0


class NewGamePlus(Choice):
    """
    Puts the castle in new game plus mode which vastly increases enemy level,
    but increases gold gain by 50%. Not recommended for those inexperienced to
    Rogue Legacy!
    """
    displayname = "New Game Plus"
    option_normal = 0
    option_new_game_plus = 1
    alias_hard = 1
    default = 0


class TotalLocations(Range):
    displayname = "Total Locations"
    range_start = 163
    range_end = 367
    default = 200


legacy_options: typing.Dict[str, Option] = {
    "starting_gender": StartingGender,
    "new_game_plus": NewGamePlus,
    "total_locations": TotalLocations
}
