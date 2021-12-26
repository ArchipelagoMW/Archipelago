from Options import Choice, Option
import typing


class InitialGender(Choice):
    """
    Determines the gender of your initial 'Sir Lee' character.
    """
    displayname = "Initial Gender"
    option_sir = 0
    option_lady = 1
    alias_male = 0
    alias_female = 1
    default = 0


class NewGamePlusMode(Choice):
    """
    Puts the castle in new game plus mode which vastly increases enemy level, but increases gold gain by 50%. Not
    recommended for those inexperienced to Rogue Legacy!
    """
    displayname = "New Game Plus Mode"
    option_normal = 0
    option_new_game_plus = 1
    alias_hard = 1
    default = 0


legacy_options: typing.Dict[str, Option] = {
    "initial_gender": InitialGender,
    "new_game_plus_mode": NewGamePlusMode,
}
