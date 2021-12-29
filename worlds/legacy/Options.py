import typing

from Options import Choice, Range, Option, DeathLink, DefaultOnToggle


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
    Puts the castle in new game plus mode which vastly increases enemy level, but increases gold gain by 50%. Not
    recommended for those inexperienced to Rogue Legacy!
    """
    displayname = "New Game Plus"
    option_normal = 0
    option_new_game_plus = 1
    alias_hard = 1
    default = 0


class FairyChestsPerZone(Range):
    """
    Determines the number of Fairy Chests in a given zone that contain items. After these have been checked, only stat
    bonuses can be found in Fairy Chests.
    """
    displayname = "Fairy Chests Per Zone"
    range_start = 5
    range_end = 50
    default = 5


class ChestsPerZone(Range):
    """
    Determines the number of Non-Fairy Chests in a given zone that contain items. After these have been checked, only
    gold or stat bonuses can be found in Chests.
    """
    displayname = "Chests Per Zone"
    range_start = 15
    range_end = 100
    default = 25


class ItemsEveryNthChests(Range):
    """
    Determines how many chests need to be opened before an item can be found. Iron and Gold chests always have items.
    """
    displayname = "Items Every Nth Chests"
    range_start = 1
    range_end = 5
    default = 2


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


class RequirePurchasingEquipment(DefaultOnToggle):
    """
    Determines where you will be required to purchase equipment from the Blacksmith before equipping them.
    """
    displayname = "Require Purchasing Equipment"


class RequirePurchasingRunes(DefaultOnToggle):
    """
    Determines where you will be required to purchase runes from the Enchantress before equipping them.
    """
    displayname = "Require Purchasing Runes"


class GoldGainMultiplier(Choice):
    """
    Adjusts the multiplier for gaining gold from all sources.
    """
    displayname = "Gold Gain Multiplier"
    option_quarter = 0
    option_half = 1
    option_normal = 2
    option_double = 3
    option_quadruple = 4
    default = 2


legacy_options: typing.Dict[str, type(Option)] = {
    "starting_gender": StartingGender,
    "new_game_plus": NewGamePlus,
    "fairy_chests_per_zone": FairyChestsPerZone,
    "chests_per_zone": ChestsPerZone,
    "items_every_nth_chests": ItemsEveryNthChests,
    "vendors": Vendors,
    "require_purchasing_equipment": RequirePurchasingEquipment,
    "require_purchasing_runes": RequirePurchasingRunes,
    "gold_gain_multiplier": GoldGainMultiplier,
    "death_link": DeathLink,
}
