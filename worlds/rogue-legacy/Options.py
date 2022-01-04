import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle


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


class StartingClass(Choice):
    """
    Determines the starting class of your initial 'Sir Lee' character.
    """
    displayname = "Starting Class"
    option_knight = 0
    option_mage = 1
    option_barbarian = 2
    option_knave = 3
    default = 0


class NewGamePlus(Choice):
    """
    Puts the castle in new game plus mode which vastly increases enemy level, but increases gold gain by 50%. Not
    recommended for those inexperienced to Rogue Legacy!
    """
    displayname = "New Game Plus"
    option_normal = 0
    option_new_game_plus = 1
    option_new_game_plus_2 = 2
    alias_hard = 1
    alias_brutal = 2
    default = 0


class FairyChestsPerZone(Range):
    """
    Determines the number of Fairy Chests in a given zone that contain items. After these have been checked, only stat
    bonuses can be found in Fairy Chests.
    """
    displayname = "Fairy Chests Per Zone"
    range_start = 5
    range_end = 15
    default = 5


class ChestsPerZone(Range):
    """
    Determines the number of Non-Fairy Chests in a given zone that contain items. After these have been checked, only
    gold or stat bonuses can be found in Chests.
    """
    displayname = "Chests Per Zone"
    range_start = 15
    range_end = 30
    default = 15


class Vendors(Choice):
    """
    Determines where to place the Blacksmith and Enchantress unlocks in logic (or start with them unlocked).
    """
    displayname = "Vendors"
    option_start_unlocked = 0
    option_early = 1
    option_normal = 2
    option_anywhere = 3
    default = 1


class DisableCharon(Toggle):
    """
    Prevents Charon from taking your money when you re-enter the castle. Also removes Haggling from the Item Pool.
    """
    displayname = "Disable Charon"


class RequirePurchasing(DefaultOnToggle):
    """
    Determines where you will be required to purchase equipment and runes from the Blacksmith and Enchantress before
    equipping them. If you disable require purchasing, Manor Renovations are scaled to take this into account.
    """
    displayname = "Require Purchasing"


class GoldGainMultiplier(Choice):
    """
    Adjusts the multiplier for gaining gold from all sources.
    """
    displayname = "Gold Gain Multiplier"
    option_normal = 0
    option_quarter = 1
    option_half = 2
    option_double = 3
    option_quadruple = 4
    default = 0


class NumberOfChildren(Range):
    """
    Determines the number of offspring you can choose from on the lineage screen after a death.
    """
    displayname = "Number of Children"
    range_start = 1
    range_end = 5
    default = 3


legacy_options: typing.Dict[str, type(Option)] = {
    "starting_gender": StartingGender,
    "starting_class": StartingClass,
    "new_game_plus": NewGamePlus,
    "fairy_chests_per_zone": FairyChestsPerZone,
    "chests_per_zone": ChestsPerZone,
    "vendors": Vendors,
    "disable_charon": DisableCharon,
    "require_purchasing": RequirePurchasing,
    "gold_gain_multiplier": GoldGainMultiplier,
    "number_of_children": NumberOfChildren,
    "death_link": DeathLink,
}
