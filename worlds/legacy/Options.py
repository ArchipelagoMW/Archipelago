from Options import Choice, Option, OptionList, Range, DeathLink, Toggle
import typing

class InitialGender(Choice):
    """Determines the gender of your initial character."""
    displayname = "Initial Gender"
    option_sir = 0
    option_lady = 1
    alias_male = 0
    alias_female = 1
    default = 0


class Difficulty(Choice):
    """Determines game difficulty based off New Game + difficulties."""
    displayname               = "Difficulty"
    option_normal             = 0
    option_hard               = 1
    option_brutal             = 2
    option_near_impossible    = 3
    alias_new_game_plus       = 1
    alias_new_game_plus_two   = 2
    alias_new_game_plus_three = 3
    alias_devastating         = 3  # Just for you Dori
    default                   = 0


class StatIncreasePool(Range):
    """Determines the number of stat increase packs in the pool."""
    displayname = "Stat Increase Pool"
    range_start = 0
    range_end   = 150
    default     = 50


class EarlyVendors(Choice):
    """Puts Vendors earlier in the pool or later. Inspired by Early Morph from Varia Randomizer."""
    displayname = "Early Vendors"
    option_early = 0
    option_normal = 1
    default = 0


class BossShuffle(Choice):
    """Whether or not to shuffle the 4 main bosses (excluding Johannes) amongst themselves. Enabled Set - Shuffles them once, but each boss will stay in their respective zone. Enabled Random - Shuffles them everytime the castle layout is regenerated."""
    displayname           = "Boss Shuffle"
    option_disabled       = 0
    option_enabled_set    = 0
    option_enabled_random = 0


class Children(Range):
    """Determines the amount of children the player can choose from after a death."""
    displayname = "Children"
    range_start = 1
    range_end   = 5
    default     = 3


class EnableShop(Toggle):
    """Determine whether the player can buy from the Manor Shop. Recommended to have higher Stat Increase Pool when using this setting."""
    displayname = "Enable Shop"
    default     = 1


class AdditionalChildrenNames(OptionList):
    """Adds additional names to the name pool for your children."""
    displayname = "Possible Children Names"


class AllowVendorsInCastle(Toggle):
    """If unlocked, spawns the Blacksmith and Enchantress in Diary Rooms."""
    displayname = "Allow Vendors in Castle"
    default = 0


class DisableCharon(Toggle):
    """Prevents Charon from taking your money when entering Castle Hamson. Removes Haggles from the Item Pool."""
    displayname = "Disable Charon"
    default = 0


class HereditaryBlessings(Toggle):
    """Blessings your character aquires are passed onto your children after death."""
    displayname = "Hereditary Blessings"
    default = 0


class StatIncreaseApplies(Choice):
    """Determines whether AP-given stat increase packs apply to your current character or after death. Not recommended with DeathLink."""
    displayname = "Stat Increase Applies..."
    option_immediately = 0
    option_after_death = 1
    default = 0


class RoomRandomizer(Toggle):
    """Shuffles rooms from every area into every other area. Who knows what you'll get!"""
    displayname = "Area Randomizer"
    default = 0


legacy_options: typing.Dict[str, type(Option)] = {
    "initial_gender": InitialGender,
    "difficulty": Difficulty,
    "stat_increase_pool": StatIncreasePool,
    "stat_increase_applies": StatIncreaseApplies,
    "early_vendors": EarlyVendors,
    "boss_shuffle": BossShuffle,
    "children": Children,
    "hereditary_blessings": HereditaryBlessings,
    "enable_shop": EnableShop,
    "disable_charon": DisableCharon,
    "death_link": DeathLink,
    "additional_children_names": AdditionalChildrenNames,
}
